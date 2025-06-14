import json
import globals
import os

def setup_opentd():
    if not os.path.exists("opentd.json"):
        raise FileNotFoundError("cannot find opentd.json")
    
    with open("opentd.json", "r") as file:
        content = json.load(file)

    globals.json_assets["settings"] = content

def colour_from_table(table):
    return (
        int(table["r"]),
        int(table["g"]),
        int(table["b"]),
    )