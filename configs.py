import requests
import json

def fetch_swagger_data(swagger_url):
    try:
        response = requests.get(swagger_url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching Swagger data. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching Swagger data: {e}")
        return None

def extract_config(swagger_data, endpoint_path):
    try:
        paths = swagger_data.get('paths', {})
        endpoint_data = paths.get(endpoint_path, {})
        return endpoint_data
    except Exception as e:
        print(f"Error extracting config: {e}")
        return None

def save_config(config_data, output_file):
    try:
        with open(output_file, 'w') as f:
            json.dump(config_data, f, indent=4)
        print(f"Config data saved to {output_file}")
    except Exception as e:
        print(f"Error saving config data: {e}")

if __name__ == "__main__":
    swagger_url = "http://localhost:8080/v2/api-docs"
    endpoint_path = "/schema-extractor-rest/v2/endpoint/buildFullSchema"
    output_file = "config_data.json"

    swagger_data = fetch_swagger_data(swagger_url)
    if swagger_data:
        config_data = extract_config(swagger_data, endpoint_path)
        if config_data:
            save_config(config_data, output_file)
