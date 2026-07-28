import json
from pathlib import Path

LOCATIONS = {
    "Rocky Plateau": "rocky_plateau",
    "Deadwood Canyon": "deadwood_valley",
    "Caves of Fear": "caustic_caves",
    "Mushroom Forest": "fungus_forest",
    "Haunted Halls": "undead_crypt",
    "Boiling Mine": "bronze_mine",
    "Icy Ridge": "icy_ridge",
    "Temple": "temple",
}


def load_from_xlsx(sheet_path):
    import openpyxl

    LOCATION_VALUES: dict[str, float] = {}

    ROWS = [55, 64, 73, 82, 91, 100, 109, 118]

    wb = openpyxl.load_workbook(sheet_path, data_only=True)
    ws = wb["Chest Rates"]

    for row in ROWS:
        name = str(ws.cell(row, 2).value)
        values = [float(ws.cell(row + 7, col).value) for col in range(4, 20)]

        loc_id = LOCATIONS[name]
        star = 5

        for v in values:
            LOCATION_VALUES[loc_id + str(star)] = float(v)
            star += 1

    return LOCATION_VALUES


def load_from_json(json_path):
    try:
        with open(json_path, "r") as f:
            loaded: dict[str, float] = json.load(f)
            return loaded
    except FileNotFoundError:
        print("file doesn't exist")
    except json.JSONDecodeError:
        print("file exists but isn't valid JSON")


# todo: maybe later we add emerald egg chances / other rates too


def save_json(json_path, data):
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)


def get_location_values():
    script_location = Path(__file__).parent
    sheet_path = script_location / "chest_rates.xlsx"
    json_path = script_location / "chest_rates.json"

    if sheet_path.exists():
        try:
            data = load_from_xlsx(sheet_path)
            save_json(json_path, data)
            return data
        except ImportError:
            print("openpyxl not found, try installing")

    print("sheet not found, using cache")
    return load_from_json(json_path)
