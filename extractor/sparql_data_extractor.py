from extractor.sparql_queries import SPARQLQueries

class SPARQLDataExtractor:
    """
    Data extracting from SPARQL Endpoint 
    """
    __sparql_queries = SPARQLQueries()
    __endpoint_data = {
        'classes': -1,
        'properties': -1,
        'triples': -1,
        'unique_properties': -1
    }

    __most_used_properties = [
        {
            'iri': '',
            'count': -1,
            'object_count': -1
        },
        {
            'iri': '',
            'count': -1,
            'object_count': -1
        },
        {
            'iri': '',
            'count': -1,
            'object_count': -1
        },
        {
            'iri': '',
            'count': -1,
            'object_count': -1
        }
    ]

    def __test_connection(self):
        """ Verify connection to the given endpoint """
        try:
            self.__sparql_queries.test_connection()
            
            return True
        except Exception as e:
            print(e)
            return False

    def is_instance_valid(self, url):
        self.__sparql_queries.set_wrapper(url)

        if self.__test_connection() == False:
            print('error')
            return False
        
        return self.__sparql_queries.get_instances_count()

    def extract_data(
        self,
        access_url,
    ):
        """ Makes SPARQL calls on the endpoint and fetches data """
        self.__sparql_queries.set_wrapper(access_url)

        if self.__test_connection() == False:
            return []

        self.__endpoint_data['classes'] = self.__sparql_queries.get_classes_count()
        self.__endpoint_data['properties'] = self.__sparql_queries.get_properties_count()
        self.__endpoint_data['triples'] = self.__sparql_queries.get_triples_count()

        if self.__endpoint_data['classes'] > -1 and self.__endpoint_data['properties'] == 0:
            self.__endpoint_data['unique_properties'] = self.__sparql_queries.get_unique_properties_count()
        
        return self.__endpoint_data

    def get_most_used_properties_data(self, access_url):
        return self.__most_used_properties
    
        self.__sparql_queries.set_wrapper(access_url)

        properties = self.__sparql_queries.get_two_most_used_properties()
        for index, property in enumerate(properties):
            self.__most_used_properties[index]['iri'] = property['p']['value']
            self.__most_used_properties[index]['count'] = property['px']['value']
            self.__most_used_properties[index]['object_count'] = self.__sparql_queries.get_distinct_object_count(property['p']['value'])
        
        return self.__most_used_properties