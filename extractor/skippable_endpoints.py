import os
import csv

class SkippableEndpoints:
    """ 
    Gathering of endpoitns to skip
    """
    def get_endpoints_to_skip(self, queries_from_source = False):
        """ Returns a list of endpoints to skip """
        endpoints_to_skip = []

        if queries_from_source:
            with open('./' + os.getenv('SKIPPABLE_ENDPOINTS_FILE'), 'r') as csvfile:
                csvreader = csv.reader(csvfile)

                for row in csvreader:
                    if len(row) == 0:
                        continue
                    
                    endpoints_to_skip.append(row[0].strip())
        with open(os.getenv('EXTRACTION_STATISTICS_OUTPUT'), 'r') as csv_file:
            csvreader = csv.reader(csv_file, delimiter=';')

            for row in csvreader:
                endpoints_to_skip.append(row[0])

        return endpoints_to_skip
