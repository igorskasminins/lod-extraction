import os
import csv

class StatsReader:
    """ Extraction results manager """
    __csv_writer = None

    def __initWriter(self, csv_file):
        """ Initialize the CSV writer with configuration """
        self.__csv_writer = csv.writer(csv_file, delimiter=';')

    def write_data(
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
                properties_count_triples,
                properties_count_data_triples,
                triples_count_expected, 
                json_output_file,
                api_call_request,
                error
            ])