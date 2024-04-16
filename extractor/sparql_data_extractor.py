from extractor.sparql_queries import SPARQLQueries

class SPARQLDataExtractor:
    """
    Data extracting from SPARQL Endpoint 
    """

    __endpoint_data = {
        'classes': -1,
        'properties': -1,
        'triples': -1,
        'unique_properties': -1
    }

    def __init__(self):
        self.sparql_queries = SPARQLQueries()

    def __test_connection(self):
        """ Verify connection to the given endpoint """
        try:
            self.sparql_queries.test_connection()
            
            return True
        except Exception:
            return False

    def extract_data(
        self,
        access_url,
    ):
        """ Makes SPARQL calls on the endpoint and fetches data """
        self.sparql_queries.set_wrapper(access_url)

        if self.__test_connection() == False:
            return []

        self.__endpoint_data['classes'] = self.sparql_queries.get_classes_count()
        self.__endpoint_data['properties'] = self.sparql_queries.get_properties_count()
        self.__endpoint_data['triples'] = self.sparql_queries.get_triples_count()

        if self.__endpoint_data['classes'] > -1 and self.__endpoint_data['properties'] == 0:
            self.__endpoint_data['unique_properties'] = self.sparql_queries.get_unique_properties_count()
        
        return self.__endpoint_data

