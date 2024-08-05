from get_data_from_expo import fetch_data_from_graphql
import json
import yaml

def read_secrets(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

secrets_file_path = './secrets.yaml'

secrets = read_secrets(secrets_file_path)
token = secrets['token']
endpoint = secrets['endpoint']
start_date = secrets['start_date']
end_date = secrets['end_date']

def write_response_to_file_for_debug(jsondata):
    with open('debug_response.json', 'w') as file:
        file.write(json.dumps(jsondata, indent=4))
    print("Response written to file response.json")
    return


write_response_to_file_for_debug(fetch_data_from_graphql(start_date, end_date, token, endpoint))