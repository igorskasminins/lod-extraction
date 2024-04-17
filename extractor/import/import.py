import subprocess
import os
import json
import shutil
import requests
from bs4 import BeautifulSoup

folder_path = "./scripts/responses"

files = os.listdir(folder_path)

for response in files:
    with open("./scripts/responses/" + response, 'r') as json_file:
        data = json.load(json_file)

    responseSchema = os.path.splitext(response)[0]
    responseSchema = responseSchema.replace("-", "_")
    env_file_path = ".env"

    with open(env_file_path, 'r') as file:
        lines = file.readlines()

    new_lines = []

    url = "null"

    if "Parameters" in data:
        if "endpointUrl" in data["Parameters"]:
            url = data["Parameters"]["endpointUrl"]

    type = 'default'

    request = False

    try:
        request = requests.get(url)
    except:
        pass
    
    if request and request.ok:
        soup = BeautifulSoup(request.content, features='xml')
        title = soup.title

        if title:
            if title.string.lower().find('virtuoso') != -1:
                type = 'virtuoso'

    for line in lines:
        if line.startswith("SPARQL_URL="):
            line = "SPARQL_URL=" + url + "\n"
        elif line.startswith("DB_SCHEMA="):
            line = "DB_SCHEMA=" + responseSchema.lower() + "\n"
        elif line.startswith("INPUT_FILE="):
            line = "INPUT_FILE=" + './responses/' + response + "\n"
        elif line.startswith("SCHEMA_DISPLAY_NAME="):
            line = "SCHEMA_DISPLAY_NAME=" + url + "\n"
        elif line.startswith("PUBLIC_URL="):
            line = "PUBLIC_URL=" + url + "\n"
        elif type and line.startswith("ENDPOINT_TYPE="):
            line = "ENDPOINT_TYPE=" + type + "\n"

        new_lines.append(line)

    with open(env_file_path, 'w') as file:
        file.writelines(new_lines)

    os.system('npm run auto')
    shutil.move("./scripts/responses/" + response, "./scripts/processed/" + response)
