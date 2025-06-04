import json
import os
import pygame
import globals

class Map:
    def __init__(self, path):
        self.map_path = path
        
        with open(os.path.join(self.map_path, "settings.json")) as f:
            self.settings = json.load(f)

        self.colour = pygame.image.load(os.path.join(self.map_path, self.settings["image_data"]["colour"]))

    def update(self):
        globals.game_surface.blit(self.colour, (0,0))