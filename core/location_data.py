import json


def load_from_json(json_path):
    try:
        with open(json_path, "r") as f:
            loaded: dict[str, float] = json.load(f)
            return loaded
    except FileNotFoundError:
        print("file doesn't exist")
    except json.JSONDecodeError:
        print("file exists but isn't valid JSON")


def save_json(json_path, data):
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)
