import requests
import json
import csv
from read import XMLFileReader
import time
import logging

class MakeApiCall:
    def __init__(self):
        self.stats_reader = StatsReader()
        self.logger = Logger()
        self.json_reader = JsonReader()

    def construct_endpoint_url(self, base_url, config_data):
        query_string = '&'.join([f"{key}={value}" for key, value in config_data.items()])
        endpoint_url = f"{base_url}?{query_string}"

        return endpoint_url

    def get_data(self):
        reader = XMLFileReader()
        urls = reader.getUrls()

        config_data = self.json_reader.getConfigData()
        fixed_api_endpoint = 'http://localhost:8080/schema-extractor-rest/v2/endpoint/buildFullSchema'

        for url, endpoint_data in urls.items():
            start = time.time()
            
            config_data['endpointUrl'] = url

            full_endpoint_url = self.construct_endpoint_url(fixed_api_endpoint, config_data)
            self.logger.printAndLogInfo(f'Starting extraction for {url}')

            try:
                response = requests.post(full_endpoint_url)
            except Exception as exception:
                self.logger.printAndLogError(f'The connection could not have been established with {url} for the following request: {full_endpoint_url}')

                self.stats_reader.writeData(
                    access_url=url,
                    api_call_request=full_endpoint_url,
                    error=exception
                )

                continue

            if response.status_code == 200:
                output_file = endpoint_data['output_file']
                end = time.time()
                elapsed_time = int(round(end - start, 2) * 1000)

                response_result = response.json()
                self.json_reader.saveResponse(response_result, output_file, elapsed_time)
                classes = self.json_reader.extractClassesDataFromJson()
                props = self.json_reader.extractPropertiesDataFromJson()

                self.stats_reader.writeData(
                    url, 
                    elapsed_time, 
                    self.json_reader.hasErrors(), 
                    endpoint_data['classes'], 
                    classes['actual_classes'],
                    classes['classes_instance_count'],
                    classes['classes_inc_tr_cnt'],
                    endpoint_data['properties'],
                    props['actual_properties'],
                    props['actual_prop_triples'],
                    props['actual_prop_data_triples'],
                    endpoint_data['triples'], 
                    output_file,
                    full_endpoint_url,
                    'NULL'
                )

            else:
                error_msg = ''

                try:
                    error_msg = response.json()
                except:
                    error_msg = 'Could not save the message'

                self.stats_reader.writeData(
                    access_url=url,
                    api_call_request=full_endpoint_url,
                    error=error_msg
                )

                self.logger.printAndLogError(f"Error: {response.status_code}. Failed to fetch data from URL {url}")
                self.logger.printAndLogError(f"Response content: {response.content}")

    def __init__(self):
        self.get_data()

if __name__ == "__main__":
    api_call = MakeApiCall()

class Logger:
    def __init__(self):
        logging.basicConfig(
            format='%(asctime)s %(levelname)-8s %(message)s',
            filename='system.log', 
            level=logging.INFO,
            datefmt='%Y-%m-%d %H:%M:%S'
        )
                
        self.logger = logging.getLogger()

    def printAndLogInfo(self, message):
        self.logger.info(message)
        print(message)

    def printAndLogError(self, message):
        self.logger.error(message)
        print(message)

class JsonReader:
    __json_data = None

    def __init__(self):
        self.logger = Logger()
        pass

    def getConfigData(self, filename='config_data.json'):
        with open(filename, 'r') as config_file:
            config_data = json.load(config_file)

        return config_data

    def saveResponse(self, json_data, filename, elapsed_time):
        self.__json_data = json_data
        with open(f'responses/{filename}.json.', 'w') as outfile:
            json.dump(
                self.__json_data, 
                outfile, 
                sort_keys=True, 
                indent=4
            )
            self.logger.printAndLogInfo(f"Response saved to {filename} Elapsed time {elapsed_time}")


    def extractPropertiesDataFromJson(self):
        actual_properties = 0
        actual_prop_triples = 0
        actual_prop_data_triples = 0

        if 'Properties' in self.__json_data:
            actual_properties = len(self.__json_data['Properties'])

            for prop in self.__json_data['Properties']:
                actual_prop_triples += prop['tripleCount']
                actual_prop_data_triples += prop['dataTripleCount']

        return {
            'actual_properties': actual_properties,
            'actual_prop_triples': actual_prop_triples,
            'actual_prop_data_triples': actual_prop_data_triples
        }

    def extractClassesDataFromJson(self):
        actual_classes = 0
        classes_instance_count = 0
        classes_inc_tr_cnt = 0
        if 'Classes' in self.__json_data:
            actual_classes = len(self.__json_data['Classes'])
            for clas in self.__json_data['Classes']:
                classes_instance_count += clas['instanceCount']
                if 'incomingTripleCount' in clas:
                    classes_inc_tr_cnt += clas['incomingTripleCount']

        return {
            'actual_classes': actual_classes,
            'classes_instance_count': classes_instance_count,
            'classes_inc_tr_cnt': classes_inc_tr_cnt
        }
    
    def hasErrors(self):
        if 'HasErrors' in self.__json_data:
            self.__json_data['HasErrors'] == True
        else:
            return 'NULL'

class StatsReader:
    STATISTICS = 'statistics.csv'
    __csv_writer = None

    def __initWriter(self, csv_file):
        self.__csv_writer = csv.writer(csv_file, delimiter=';')

    def writeData(
        self,
        access_url = 'NULL', 
        elapsed_time = 'NULL', 
        json_has_errors = 'NULL', 
        classes_count_expected = 'NULL', 
        classes_count = 'NULL',
        classes_instance_count = 'NULL',
        classes_incoming_triple_count = 'NULL',
        properties_count_expected = 'NULL',
        properties_count = 'NULL',
        properties_count_triples = 'NULL',
        properties_count_data_triples = 'NULL',
        triples_count_expected = 'NULL', 
        json_output_file = 'NULL',
        api_call_request = 'NULL',
        error = 'NULL'
    ):
        with open(self.STATISTICS, 'a', newline='') as csv_file:
            self.__initWriter(csv_file)

            self.__csv_writer.writerow([
                access_url, 
                elapsed_time, 
                json_has_errors, 
                classes_count_expected, 
                classes_count,
                classes_instance_count,
                classes_incoming_triple_count,
                properties_count_expected,
                properties_count,
                properties_count_triples,
                properties_count_data_triples,
                triples_count_expected, 
                json_output_file,
                api_call_request,
                error
            ])