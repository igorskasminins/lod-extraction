# Schema Extraction Tool for OBIS

The program provides an automated approach for extracting LOD schemas from endpoints using [OBIS-SchemaExtractor](https://github.com/LUMII-Syslab/OBIS-SchemaExtractor):

There are available 2 options for providing endpoints. Both of which should be executed from **root** directory.

The overview of the extraction process is saved in the _extraction_statistics_output.csv_ file.

The output of successfull extraction is available under the _responses_ directory as _.JSON_ files.

<br>

# Installation

The following conditions mustbe met:

1. Python3 is installed

2. Pip is installed

3. Run the command from root directory to install necessary python modules:


```
pip install -r requirements.txt
```

In case of errors related to missing/unaccasable files, try:
```
pip install -r requirements.txt --user
```
# Available commands


All the commands must be executed from the root directory (_lod-extraction_ by default)

### 1. Extracting endpoints from http://85.254.199.72:8890/sparql.
<br>

At first a query defined in _source_qurey.txt_ will be executed on the source and endpoints will be retrieved for further extraction.

Additionaly, there is available a file _endpoints-to-skip.csv_ with endpoints that will be skipped for extraction.

Command to start the extraction from the source. 
```
python -m extraction start-source
```
<br>

### 2. Providing own list of endpoints.
<br>

The list of endpoints for extraction should be provided in _./endpoints/custom-endpoints.csv_ file. Where each endpoint should be separated by a new line.

```
python -m extraction start-file
```
<br>

# Import to PostgresSQL - Data Shape Server ([DSS](https://github.com/LUMII-Syslab/data-shape-server))

Additionally, after successfull installation of the server and set up of the first database with necessary schema templates, there is a script avalable that can perform bulk upload of the extracated schemas under _extractor/import_ directory. The script must be placed under _import-generic_ directory and under _import-generic/scripts_ directory of DSS.

So that the contents of _scripts_ wolud look like this:

![alt text](https://github.com/igorskasminins/lod-extraction/blob/main/img/example.jpg?raw=true)


The _processed_ directory will be created automatically to stored already processed schemas.

After that the python script can be executed from the _import-generic_ directory which will perform the import of all the schemas located inside _response_ directory to the database with the following:

```
python import.py
```

Additionally, to skip the authentication for DB you can modify the contents of _createSchema_ function inside _main.js_ so that it would look like this, which is the laternative way of providing credentials inside the commands:

For example:

user: postgres
<br>
passoword: admin
<br>
DB port: 5432
<br>
DB name: extraction
```
await $`pg_dump -E UTF8 --dbname=postgres://postgres:admin@localhost:5432/extraction -n empty -f ${EMPTY_SCHEMA}.sql `;
	
await $`psql --dbname=postgres://postgres:admin@localhost:5432/extraction -c "alter schema ${EMPTY_SCHEMA} rename to ${schemaName}"`

await $`psql --dbname=postgres://postgres:admin@localhost:5432/extraction -f ${EMPTY_SCHEMA}.sql `;
```

Another alternative would be defining _PostgrSQL_ variables on Windows level.


## ViziQuer

As of current version of recommended db-templates for for DSS, ViziQuer does not display uploaded schemas because of the missing view "public.v_configuration".

To fix the issue the following code snippet could be included in the _public-template-v2.pgsql_ before creating a base database or at any point even after scheme import by executing the SQL query:

```
--
-- Name: v_configurations; Type: VIEW; Schema: public; Owner: rdf
--

CREATE VIEW public.v_configurations AS
 SELECT s.display_name,
    s.db_schema_name,
    e.sparql_url,
    s.is_active,
    COALESCE(e.named_graph, ''::text) AS named_graph
   FROM (public.endpoints e
     JOIN public.schemata s ON ((e.id = s.endpoint_id)))
  WHERE s.is_active
  ORDER BY s.display_name;

ALTER TABLE public.v_configurations OWNER TO rdf;

--
-- Name: TABLE v_configurations; Type: ACL; Schema: public; Owner: rdf
--

GRANT SELECT ON TABLE public.v_configurations TO rdfro;
```

The following view was created based on the first version of the template and required fields for data queries.