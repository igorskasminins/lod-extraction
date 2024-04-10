import requests

# Define the SPARQL query
sparql_query = """
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

# Define the endpoint URL and dataset name
endpoint_url = "http://85.254.199.72:8890/sparql"
dataset_name = "http://sparql_endpoints.ex"

# Make the API call
response = requests.get(endpoint_url, params={"query": sparql_query, "default-graph-uri": dataset_name})

# Check if the request was successful
if response.status_code == 200:
    # Save the result to a file
    with open("sparql_results.txt", "w") as file:
        file.write(response.text)
    print("Result saved to sparql_results.txt")
else:
    print("Error: Unable to fetch data from the SPARQL endpoint.")