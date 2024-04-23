import os
import csv

class StatsReader:
    """ Extraction results manager """
    __csv_writer = None

    def __initWriter(self, csv_file):
        """ Initializes the CSV writer with configuration """
        self.__csv_writer = csv.writer(csv_file, delimiter=';')

    def write_data(
        self,
        access_url = '', 
        elapsed_time = '', 
        json_has_errors = '', 
        classes_count_expected = '', 
        classes_count = '',
        classes_instance_count = '',
        classes_incoming_triple_count = '',
        properties_count_expected = '',
        properties_count = '',
        properties_count_triples = '',
        properties_count_data_triples = '',
        triples_count_expected = '', 
        first_most_property_iri = '',
        first_most_property_count = '',
        first_most_property_object_count = '',        
        second_most_property_iri = '',
        second_most_property_count = '',
        second_most_property_object_count = '',
        json_output_file = '',
        is_extraction_full = '',
        api_call_request = '',
        endpoint_origin = '',
        error = ''
    ):
        """ 
        Saves results of extraction into the statistics file 
        """
        extraction_statistics_output = os.getenv('EXTRACTION_STATISTICS_OUTPUT')
        with open(f'./{extraction_statistics_output}', 'a', newline='') as csv_file:
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
                properties_count_data_triples,
                properties_count_triples,
                triples_count_expected, 
                first_most_property_iri,
                first_most_property_count,
                first_most_property_object_count,        
                second_most_property_iri,
                second_most_property_count,
                second_most_property_object_count,
                json_output_file,
                is_extraction_full,
                api_call_request,
                endpoint_origin,
                error
            ])
