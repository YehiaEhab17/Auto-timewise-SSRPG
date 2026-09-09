import zipfile
from pathlib import Path

from cli.xlsx_data import get_location_values

ROOT = Path(__file__).parent
OUT = ROOT / "page" / "timewise.zip"

INCLUDE = {
    "core": [
        "Rijndael.py",
        "crypto.py",
        "Slimjson.py",
        "classes.py",
        "timewise_logic.py",
        "saves.py",
        "location_data.py",
    ],
    "web": [
        "app.py",
    ],
}
ROOT_FILES = ["chest_rates.json"]


def build():
    get_location_values()

    OUT.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for pkg, names in INCLUDE.items():
            z.writestr(pkg + "/", "")
            for name in names:
                src = ROOT / pkg / name
                if not src.exists():
                    raise FileNotFoundError(f"missing source file: {src}")
                z.write(src, f"{pkg}/{name}")

        for name in ROOT_FILES:
            src = ROOT / name
            if not src.exists():
                raise FileNotFoundError(f"missing source file: {src}")
            z.write(src, name)

    print(f"wrote {OUT}")
    with zipfile.ZipFile(OUT) as z:
        for name in z.namelist():
            print(" ", name)


if __name__ == "__main__":
    build()
