import csv
from pathlib import Path

CSV_PATH = Path("./glottolog_languoid/languoid.csv")


def load_full_glottolog():
    """
    Build a dict: glottocode -> language name
    for all entries in Glottolog.
    """
    d = {}
    with open(CSV_PATH, encoding="utf8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            code = row["id"].strip()  # <- changed from 'glottocode'
            name = row["name"].strip()
            if code and name:
                d[code] = name
    return d


if __name__ == "__main__":
    full = load_full_glottolog()

    print(f"Total Glottolog codes: {len(full)}")

    # Optionally write them to Python files:
    with open("glottolog_full.py", "w", encoding="utf8") as out:
        out.write("VALID_GLOTTOLOG_CODES = {\n")
        for k, v in sorted(full.items()):
            out.write(f'    "{k}": "{v}",\n')
        out.write("}\n")
