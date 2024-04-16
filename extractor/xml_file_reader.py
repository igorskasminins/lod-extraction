import xml.etree.ElementTree as ET
from extractor.get_endpoints import EndpointRetrieval
import os
import csv

class XMLFileReader:
    """ Read contents of a XML file with endpoints, classes, properties and tripples """
    endpoint_retrieval = EndpointRetrieval()
    endpoints = {}

    def __read_urls_from_xml(self):
        endpoints_to_extract = os.getenv("ENDPOINTS_FROM_SOURCE")

        if not os.path.exists(f'./{endpoints_to_extract}'):
            self.endpoint_retrieval.retrieve_endpoints()

        tree = ET.parse(f'./{endpoints_to_extract}')

        root = tree.getroot()

        namespace = {"sparql": "http://www.w3.org/2005/sparql-results#"}

        for result in root.findall(".//sparql:result", namespace):
            urlElement = result.find("sparql:binding[@name='EffectiveURL']/sparql:uri", namespace)
            classes = result.find("sparql:binding[@name='classes']/sparql:literal", namespace)
            properties = result.find("sparql:binding[@name='properties']/sparql:literal", namespace)
            triples = result.find("sparql:binding[@name='triples']/sparql:literal", namespace)

            if urlElement is not None:
                url = urlElement.text
                self.endpoints[url] = {
                    'classes': classes.text,
                    'properties': properties.text,
                    'triples': triples.text,
                }

    def get_urls_from_source(self):
        if not self.endpoints:
            self.__read_urls_from_xml()
            
        return self.endpoints
    
    def get_custom_urls(self):
        endpoints = []

        with open('./' + os.getenv('CUSTOM_ENDPOINTS'), 'r') as csv_file:
            csvreader = csv.reader(csv_file, delimiter=';')

            for row in csvreader:
                endpoints.append(row[0])

        return endpoints
