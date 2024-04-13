import xml.etree.ElementTree as ET
from get_endpoints import EndpointRetrieval
import os
from dotenv import load_dotenv

class XMLFileReader:
    """ Read contents of a XML file with endpoints, classes, properties and tripples """
    endpoint_retrieval = EndpointRetrieval()
    endpoints = {}

    def __readUrls(self):
        endpoints_to_extract = os.getenv("ENDPOINTS_TO_EXTRACT")

        if not os.path.exists(f'../{endpoints_to_extract}'):
            self.endpoint_retrieval.retrieve_endpoints()

        tree = ET.parse(f'../{endpoints_to_extract}')

        root = tree.getroot()

        namespace = {"sparql": "http://www.w3.org/2005/sparql-results#"}

        for result in root.findall(".//sparql:result", namespace):
            urlElement = result.find("sparql:binding[@name='EffectiveURL']/sparql:uri", namespace)
            classes = result.find("sparql:binding[@name='classes']/sparql:literal", namespace)
            properties = result.find("sparql:binding[@name='properties']/sparql:literal", namespace)
            triples = result.find("sparql:binding[@name='triples']/sparql:literal", namespace)

            if urlElement is not None:
                url = urlElement.text
                file_name = url
                file_name = file_name.replace('.', '_')
                file_name = file_name.replace('//', '_')
                file_name = file_name.replace('/', '_')
                file_name = file_name.replace(':', '')

                self.endpoints[url] = {
                    'output_file': file_name,
                    'classes': classes.text,
                    'properties': properties.text,
                    'triples': triples.text,
                }

    def getUrls(self):
        if not self.endpoints:
            self.__readUrls()
            
        return self.endpoints