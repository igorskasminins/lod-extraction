import requests
from extractor.xml_file_reader import XMLFileReader
from extractor.logger import Logger
from extractor.stats_reader import StatsReader
from extractor.json_reader import JsonReader
from extractor.skippable_endpoints import SkippableEndpoints
from extractor.sparql_data_extractor import SPARQLDataExtractor
import time
import os

class ExtractorAPI:
    """
    Handling extraction calls to OBIS
    """
    __logger = Logger()
    __stats_reader = StatsReader()
    __json_reader = JsonReader()
    __endpoints_reader = XMLFileReader()
    __skippable_endpoints = SkippableEndpoints()
    __sparql_data_extractor = SPARQLDataExtractor()

    def __construct_endpoint_url(self, config_data):
        """ Constructs an API URL for calling the extraction using given parameters """
        query_string = '&'.join([f"{key}={value}" for key, value in config_data.items()])

        obis_url = os.getenv('OBIS_API')

        endpoint_url = f"{obis_url}?{query_string}"

        return endpoint_url

    def __make_request(self, url, config_data, endpoint_data, endpoint_origin):
        """ Makes a request to OBIS API endpoint """
        output_file = endpoint_data['output_file']
        
        if os.path.exists(f'./results/responses/{output_file}.json'):
            self.__logger.print_and_log_info(f'Skipping as the JSON output exists: {output_file}')

            return

        config_data['endpointUrl'] = url

        if (int(endpoint_data['properties']) > 200) or (int(endpoint_data['triples']) > 10000000):
            config_data['calculatePropertyPropertyRelations'] = False
            config_data['calculateSourceAndTargetPairs'] = False

        if int(endpoint_data['classes']) > 200:
            config_data['calculateMultipleInheritanceSuperclasses'] = False

            if int(endpoint_data['classes']) > 500:
                if int(endpoint_data['classes']) != 522:
                    config_data['minimalAnalyzedClassSize'] = 10

        full_endpoint_url = self.__construct_endpoint_url(config_data)

        most_used_properties = self.__sparql_data_extractor.get_most_used_properties_data(url)

        start = time.time()

        self.__logger.print_and_log_info(f'Starting extraction for {url}')
        self.__logger.print_and_log_info(full_endpoint_url)

        try:
            response = requests.post(full_endpoint_url)

        except Exception as exception:
            self.__logger.print_and_log_error(f'The connection could not have been established with {url} for the following request: {full_endpoint_url}')
            end = time.time()
            elapsed_time = int(round(end - start, 2) * 1000)

            self.__stats_reader.write_data(
                access_url=url,
                elapsed_time=elapsed_time,
                classes_count_expected=endpoint_data['classes'],
                properties_count_expected=endpoint_data['properties'],
                triples_count_expected=endpoint_data['triples'],
                api_call_request=full_endpoint_url,
                endpoint_origin=endpoint_origin,
                error=exception
            )

            return

        end = time.time()
        elapsed_time = int(round(end - start, 2) * 1000)

        if response.status_code == 200:
            response_result = response.json()

            if not os.path.exists('results/responses'):
                os.makedirs('results/responses')

            self.__json_reader.save_response(response_result, output_file, elapsed_time)
            classes = self.__json_reader.extract_classes_data_from_json()
            props = self.__json_reader.extract_properties_data_from_json()

            actual_class = int(classes['actual_classes'])
            expected_class = int(endpoint_data['classes'])
            actual_properties = int(props['actual_properties'])
            expected_properties = int(endpoint_data['properties'])

            is_extraction_full = False if (expected_class > 0 and actual_class == 0) or (expected_properties > 0 and actual_properties == 0) else True

            self.__stats_reader.write_data(
                url, 
                elapsed_time, 
                self.__json_reader.has_errors(), 
                endpoint_data['classes'], 
                classes['actual_classes'],
                classes['classes_instance_count'],
                classes['classes_inc_tr_cnt'],
                endpoint_data['properties'],
                props['actual_properties'],
                props['actual_prop_triples'],
                props['actual_prop_data_triples'],
                endpoint_data['triples'], 
                most_used_properties[0]['iri'],
                most_used_properties[0]['count'],
                most_used_properties[0]['object_count'],
                most_used_properties[1]['iri'],
                most_used_properties[1]['count'],
                most_used_properties[1]['object_count'],
                most_used_properties[2]['iri'],
                most_used_properties[2]['count'],
                most_used_properties[2]['object_count'],
                most_used_properties[3]['iri'],
                most_used_properties[3]['count'],
                most_used_properties[3]['object_count'],
                output_file,
                is_extraction_full,
                full_endpoint_url,
                endpoint_origin,
                ''
            )

        else:
            error_msg = ''

            try:
                error_msg = response.json()
            except:
                error_msg = 'Could not read the server error message'

            self.__stats_reader.write_data(
                access_url=url,
                elapsed_time=elapsed_time,
                classes_count_expected=endpoint_data['classes'],
                properties_count_expected=endpoint_data['properties'],
                triples_count_expected=endpoint_data['triples'],
                api_call_request=full_endpoint_url,
                endpoint_origin=endpoint_origin,
                error=error_msg
            )

            self.__logger.print_and_log_error(f"Error: {response.status_code}. Failed to fetch data from URL {url}")
            self.__logger.print_and_log_error(f"Response content: {response.content}")

    def process_endpoints_from_source(self):
        """ Reads the XML file with the data about endpoints: url, classes, parameters and triple counts """
        urls = self.__endpoints_reader.get_urls_from_source()
        endpoints_to_skip = self.__skippable_endpoints.get_endpoints_to_skip(queries_from_source=True)
    
        for url, endpoint_data in urls.items():
            if url in endpoints_to_skip:
                self.__logger.print_and_log_info(f'Skipping URL {url}')

                continue

            config_data = self.__json_reader.get_config_data()
            endpoint_data['output_file'] = self.create_output_file_name(url)

            self.__make_request(url, config_data, endpoint_data, 'source')

    def create_output_file_name(self, url):
        """ Construct json output file from SPARQL URL """
        file_name = url.lower()
        file_name = file_name.replace('.', '_')
        file_name = file_name.replace('//', '_')
        file_name = file_name.replace('/', '_')
        file_name = file_name.replace(':', '')
        # "-" symbol is not allowed for PostgresSQL schema names
        file_name = file_name.replace('-', '_')

        return file_name
    
    def process_custom_endpoints(self):
        """ Reads the XML file with the data about endpoints: url, classes, parameters and triple counts """
        endpoints_to_skip = self.__skippable_endpoints.get_endpoints_to_skip()
        endpoints = self.__endpoints_reader.get_custom_urls()
    
        if len(endpoints) == 0:
            self.__logger.print_and_log_info('There are no specified endpoints for extraction')

            return

        for url in endpoints:
            if url in endpoints_to_skip:
                self.__logger.print_and_log_info(f'Skipping URL: {url}')

                continue

            endpoint_data = self.__sparql_data_extractor.extract_data(url)
            if endpoint_data['classes'] > -1 and endpoint_data['properties'] > -1:
                config_data = self.__json_reader.get_config_data()

                endpoint_data['output_file'] = self.create_output_file_name(url)
                self.__make_request(url, config_data, endpoint_data, 'custom')
            else:
                self.__stats_reader.write_data(
                    access_url=url, 
                    error="The endpoint URL is not fully available"
                )
