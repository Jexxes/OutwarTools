import json

def read_json(file):
    with open(file, 'r') as f:
        data = json.load(f)
        return data

def write_json(file_name, data):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)
        return True


