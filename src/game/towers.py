import pygame
from engine.ui import Button
import json
import globals
import os

from util import window_to_game_coords_auto

class Tower:
    def __init__(self, image=None):
        self.placing = False
        self.position = None
        self.image = image

    def start(self):
        print("Tower placed at", self.position)

    def cancel(self):
        print("Placement cancelled")

    def update(self):
        if self.placing:
            self.position = window_to_game_coords_auto(pygame.mouse.get_pos())

    def draw(self, screen):
        if self.position and self.image:
            rect = self.image.get_rect(center=self.position)
            screen.blit(self.image, rect)

class TowerHandler:
    PREFIX = "towers/"
    def __init__(self, path):
        with open(TowerHandler.PREFIX + path + "/tower.json", "r") as f:
            self.tower_data = json.load(f)

        self.name = self.tower_data["name"]
        self.colour = pygame.image.load(TowerHandler.PREFIX + path + "/" + self.tower_data["colour"]).convert_alpha()

        self.placing_tower = None

    def setup_ui(self, index):
        col = index % 2
        row = index // 2

        x = (800 - 12.5 / 2) + col * (75 + 12.5) + 25
        y = row * (75 + 12.5) + 25

        globals.UI.append(Button(
            x, y, 75, 75, self.name, 1, True, "center", (0, 0, 0), (200, 200, 200), self.begin_placing
        ))

    def begin_placing(self):
        print(":O")
        if not self.placing_tower:
            self.placing_tower = Tower(self.colour)
            self.placing_tower.placing = True

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click - place tower
                self.placing_tower.placing = False
                self.placing_tower.start()
                self.placing_tower = None
            elif event.button == 3:  # Right click - cancel placement
                self.placing_tower.cancel()
                self.placing_tower = None

    def update(self):
        if self.placing_tower:
            self.placing_tower.update()
                
def setup():
    for file in os.listdir("towers"):
        full_path = os.path.join("towers", file)
        if os.path.isdir(full_path):
            globals.towers.append(TowerHandler(file))

def setup_ui():
    for i, tower in enumerate(globals.towers):
        tower.setup_ui(i)

def update():
    for tower in globals.towers:
        tower.update()

def draw(screen):
    for tower in globals.towers:
        if tower.placing_tower:
            tower.placing_tower.draw(screen)

def process_event(event):
    for tower in globals.towers:
        if tower.placing_tower:
            tower.process_event(event)