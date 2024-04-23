import json
import os
from extractor.logger import Logger

class JsonReader:
    """
    Reading json data from
    """
    __logger = Logger()
    __json_data = []

    def get_config_data(self):
        """ Returns default parameters for OBIS extraction call """
        with open(os.getenv('OBIS_PARAMETERS'), 'r') as config_file:
            config_data = json.load(config_file)

        return config_data

    def save_response(self, json_data, filename, elapsed_time):
        """ Saves the json response to the file """
        self.__json_data = json_data
        with open(f'./results/responses/{filename}.json', 'w') as outfile:
            json.dump(
                self.__json_data, 
                outfile, 
                sort_keys=True, 
                indent=4
            )
            
            self.__logger.print_and_log_info(f"Response saved to {filename} Elapsed time {elapsed_time}")

    def extract_properties_data_from_json(self):
        """ Extracts information on properties from the given json """
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

    def extract_classes_data_from_json(self):
        """ Extracts information on classes from the given json """
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

    def has_errors(self):
        """ Verifies existing of errors in the resulting json """
        if 'HasErrors' in self.__json_data:
            return self.__json_data['HasErrors'] == True
        else:
            return 'NULL'