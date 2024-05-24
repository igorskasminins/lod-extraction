import requests
import os
from dotenv import load_dotenv

load_dotenv() # Load configs from the .env file

class EndpointRetrieval:
  short_sparql_query = """
  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
  PREFIX n1: <http://rdf.lumii.lv/ex#>
  PREFIX void: <http://rdfs.org/ns/void#>
  SELECT ?EffectiveURL ?classes ?properties ?triples WHERE{
    ?EffectiveURL rdf:type n1:EffectiveURL.
    ?EffectiveURL void:classes ?classes.
    ?EffectiveURL void:properties ?properties.
    ?EffectiveURL void:triples ?triples.
    FILTER(?properties <= 200)
    FILTER(?triples <= 10000000)
    FILTER(NOT EXISTS{?EffectiveURL n1:isDublicate ?isDublicate. })
  }
  ORDER BY ?classes
  """

  full_sparql_query = """
  PREFIX n1: <http://rdf.lumii.lv/ex#>
  PREFIX void: <http://rdfs.org/ns/void#>

  SELECT ?EffectiveURL ?classes ?properties ?triples WHERE {
  ?EffectiveURL rdf:type n1:EffectiveURL.
    ?EffectiveURL void:classes ?classes.
  ?EffectiveURL void:properties ?properties.
    ?EffectiveURL void:triples ?triples.
  FILTER(?properties <= 10000)
  FILTER(?classes <= 10000)
  FILTER(NOT EXISTS{?EffectiveURL n1:isDublicate ?isDublicate. })
  }
    ORDER BY ?classes
  """

  sparql_query_one = """
  PREFIX n1: <http://rdf.lumii.lv/ex#>
  PREFIX void: <http://rdfs.org/ns/void#>

  SELECT ?EffectiveURL ?classes ?properties ?triples WHERE {
  ?EffectiveURL rdf:type n1:EffectiveURL.
    ?EffectiveURL void:classes ?classes.
  ?EffectiveURL void:properties ?properties.
    ?EffectiveURL void:triples ?triples.
  FILTER(?properties >= 300)
  FILTER(?triples >= 1000000)
  FILTER(?triples <= 70000000)
  FILTER(NOT EXISTS{?EffectiveURL n1:isDublicate ?isDublicate. })
  }
    ORDER BY ?properties
  """

  sparql_query_two = """
  PREFIX n1: <http://rdf.lumii.lv/ex#>
  PREFIX void: <http://rdfs.org/ns/void#>

  SELECT ?EffectiveURL ?classes ?properties ?triples WHERE {
  ?EffectiveURL rdf:type n1:EffectiveURL.
    ?EffectiveURL void:classes ?classes.
  ?EffectiveURL void:properties ?properties.
    ?EffectiveURL void:triples ?triples.
  FILTER(?classes >= 100)
  FILTER(?classes <= 700)
  FILTER(?triples <= 100000000)
  FILTER(NOT EXISTS{?EffectiveURL n1:isDublicate ?isDublicate. })
  }
    ORDER BY ?properties
  """

  sparql_query_three = """
  PREFIX n1: <http://rdf.lumii.lv/ex#>
  PREFIX void: <http://rdfs.org/ns/void#>

  SELECT ?EffectiveURL ?classes ?properties ?triples WHERE {
  ?EffectiveURL rdf:type n1:EffectiveURL.
    ?EffectiveURL void:classes ?classes.
  ?EffectiveURL void:properties ?properties.
    ?EffectiveURL void:triples ?triples.
  FILTER(?triples >= 100000000)
  FILTER(?properties >= 300)
  FILTER(?classes >= 1000)
  FILTER(NOT EXISTS{?EffectiveURL n1:isDublicate ?isDublicate. })
  }
    ORDER BY ?triples
  """

  def retrieve_endpoints(self):
    """ calls and saves the endpoints from the given source """
    response = requests.get(
    os.getenv('ENDPOINT_WITH_ACCESS_URLS'), 
      params={
        "query": self.full_sparql_query, 
        "default-graph-uri": os.getenv('DATASET_NAME')
      }
    )

    if response.status_code == 200:
        endpoints_to_extract = os.getenv("ENDPOINTS_FROM_SOURCE")

        with open(f"./endpoints/{endpoints_to_extract}", "w") as file:
            file.write(response.text)
        print(f"Result saved to {endpoints_to_extract}")
    else:
        print("Error: Unable to fetch data from the SPARQL endpoint.")
