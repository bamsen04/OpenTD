from engine.ui import Button
import json
import globals
import os

class Tower:
    PREFIX = "towers/"
    def __init__(self, path):
        with open(Tower.PREFIX + path + "/tower.json", "r") as f:
            self.tower_data = json.load(f)

        self.name = self.tower_data["name"]

    def setup_ui(self, index):
        col = index % 2
        row = index // 2

        x = (800 - 12.5 / 2) + col * (75 + 12.5) + 25
        y = row * (75 + 12.5) + 25

        globals.UI.append(Button(
            x, y, 75, 75, self.name, 1, True, "center", (0, 0, 0), (200, 200, 200), self.begin_placing
        ))


    def begin_placing(self):
        ...

def setup():
    for file in os.listdir("towers"):
        full_path = os.path.join("towers", file)
        if os.path.isdir(full_path):
            globals.towers.append(Tower(file))

def setup_ui():
    for i, tower in enumerate(globals.towers):
        tower.setup_ui(i)
