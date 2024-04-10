import xml.etree.ElementTree as ET

class XMLFileReader:
    endpoints = {}

    def __init__(self):
        self.__readUrls()

    def __readUrls(self):
        tree = ET.parse("sparql_results.txt")
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
        return self.endpoints