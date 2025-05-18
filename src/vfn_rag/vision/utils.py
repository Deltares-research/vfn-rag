import yaml

def load_yaml_key_value(file_path: str, key: str):
    """
    Reads a YAML file and returns the value associated with the given key.

    Parameters:
        file_path (str): Path to the YAML file.
        key (str): Key whose value you want to retrieve.

    Returns:
        The value associated with the key, or None if the key is not found.
    """
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            return data.get(key)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
    return None



