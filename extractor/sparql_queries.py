from SPARQLWrapper import SPARQLWrapper, JSON
from extractor.logger import Logger

class SPARQLQueries:
    """ 
    Setting up SPARQL wrapper and calling queries 
    """
    RETURN_FORMAT = JSON

    ERROR_NUMBER = -1

    __logger = Logger()
    __endpoint_url = None

    def set_wrapper(
            self,
            endpoint_url
        ):
        """ Sets the endpoint access URL and the return format for making queries """ 
        self.__endpoint_url = endpoint_url
        self.wrapper = SPARQLWrapper(endpoint_url)
        self.wrapper.setReturnFormat(self.RETURN_FORMAT)

    def test_connection(self):
        """ Tests the SPARQL endpoint connection by selecting 10 first triples """
        self.wrapper.setQuery("""
            SELECT * WHERE {?s ?p ?o} LIMIT 1
            """
        )
        result = self.wrapper.queryAndConvert()
        try:
            ok = 'results' in result
        except:
            raise Exception("Output result is not valid")
        
    def get_triples_count(self):
        """ Retrievs the total amount of triples in the dataset """
        try:
            self.__logger.print_and_log_info(f'Starting triples extraction for {self.__endpoint_url}')
            self.wrapper.setQuery("""
                SELECT (COUNT(*) AS ?count) 
                WHERE {
                    ?s ?p ?o
                }
                """
            )

            result = self.wrapper.queryAndConvert()['results']['bindings']

            return int(result[0]['count']['value'])
        except Exception as e:
            self.__logger.print_and_log_error(f'An error occurred while executing the triples retrieval query for: {self.__endpoint_url}. {e}')

            return self.ERROR_NUMBER
        
    def get_classes_count(self):
        """ Retrievs classes from the given endpoint """
        try:
            self.__logger.print_and_log_info(f'Starting class extraction for {self.__endpoint_url}')

            self.wrapper.setQuery("""
                select ?c (count(?x) as ?cx) where {?x a ?c} 
                """
            )

            result = self.wrapper.queryAndConvert()['results']['bindings']

            return len(result)
        except Exception as e:
            self.__logger.print_and_log_error(f'An error occurred while executing the class retrieval query for: {self.__endpoint_url}. {e}')

            return self.ERROR_NUMBER
        
    def get_properties_count(self):
        """ Retrievs properties from the given endpoint """
        try:
            self.__logger.print_and_log_info(f'Starting properties extraction for {self.__endpoint_url}')

            self.wrapper.setQuery("""
                select ?p (count(?x) as ?px) where {?x ?p ?y} 
                """
            )

            result = self.wrapper.queryAndConvert()['results']['bindings']

            return len(result)
        except Exception as e:
            self.__logger.print_and_log_error(f'An error occurred while executing the property retrieval query for: {self.__endpoint_url}. {e}')

            return self.ERROR_NUMBER
        
    def get_unique_properties_count(self):
        """ Retrievs unique properties from the given endpoint """
        try:
            self.__logger.print_and_log_info(f'Starting unique properties extraction for {self.__endpoint_url}')

            self.wrapper.setQuery("""
                select distinct ?p where {?x ?p ?y}.
                """
            )

            result = self.wrapper.queryAndConvert()['results']['bindings']
            self.__test_result(result)
            
            return int(result)
        except Exception as e:
            self.__logger.print_and_log_error(f'An error occurred while executing the unique query retrieval for: {self.__endpoint_url}. {e}')

            return self.ERROR_NUMBER