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

# Available commands

## 1. Extracting endpoints from http://85.254.199.72:8890/sparql.

<br>

At first a query defined in _source_qurey.txt_ will be executed on the source and endpoints will be retrieved for further extraction.

Additionaly, there is available a file _endpoints-to-skip.csv_ with endpoints that will be skipped for extraction.

Command to start the extraction from the source. 
```
python -m extraction start-source
```
<br>

## 2. Providing own list of endpoints.
<br>

The list of endpoints for extraction sohuld be inserted into _endpoints.csv_ file. Where each endpoint should be separated by a new line.

```
python -m extraction start-file
```
<br>

# Import to PostgresSQL - Data Shape Server ([DSS](https://github.com/LUMII-Syslab/data-shape-server))

Additionally, after successfull installation of the server and set up of the first database with necessary schema template, there is a script avalable that can perform bulk upload of the extracated schemas under _extractor/import_ directory. The script could be placed with _exrtaction_statistics_output.csv_ and responses directory under import_generic/scripts directory of DSS.

So that the contents of _scripts_ woud look like this:

_responses_<br>
_exrtaction_statistics_output.csv_<br>
_import.py_<br>
_..._<br>
_json-importer.js_<br>
_main.js_<br>
_..._<br>

After that the python file can be run from the _scripts_ directory which will perform the import of all the schemas located inside _response_ directory to the database:

```
python import.py
```
