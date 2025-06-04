# Outside imports
import pygame
import argparse
import os
import sys

# Inside imports
import globals
import game.runtime
import engine.datahandler

# Initialize Pygame
pygame.init()

# Initialize argparse
parser = argparse.ArgumentParser(description="Indicates where assets are located.")
parser.add_argument("assets", help="Path to assets folder")
args = parser.parse_args()

# CD into assets..
os.chdir(args.assets)

# Initialize data
engine.datahandler.setup_opentd()

# Create pygame window
window = pygame.display.set_mode(globals.BASE_WINDOW_SIZE, pygame.RESIZABLE)
pygame.display.set_caption(globals.json_assets["settings"]["window_title"])

globals.game_surface = pygame.Surface((globals.VIEWABLE_WIDTH, globals.VIEWABLE_HEIGHT))
background_art = pygame.image.load("image/background.jpg").convert()
clock = pygame.time.Clock()

# Initialize game
game.runtime.init()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            window = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    w, h = window.get_width(), window.get_height()

    art_aspect = background_art.get_width() / background_art.get_height()
    win_aspect = w / h

    if win_aspect > art_aspect:
        scaled_height = int(w / art_aspect)
        scaled_bg = pygame.transform.smoothscale(background_art, (w, scaled_height))
        offset_y = (scaled_height - h) // 2
        window.blit(scaled_bg, (0, -offset_y))
    else:
        scaled_width = int(h * art_aspect)
        scaled_bg = pygame.transform.smoothscale(background_art, (scaled_width, h))
        offset_x = (scaled_width - w) // 2
        window.blit(scaled_bg, (-offset_x, 0))

    game.runtime.update()

    if w / h > globals.VIEWABLE_ASPECT:
        scaled_height = h
        scaled_width = int(h * globals.VIEWABLE_ASPECT)
    else:
        scaled_width = w
        scaled_height = int(w / globals.VIEWABLE_ASPECT)

    scaled_view = pygame.transform.smoothscale(globals.game_surface, (scaled_width, scaled_height))

    x = (w - scaled_width) // 2
    y = (h - scaled_height) // 2
    window.blit(scaled_view, (x, y))

    pygame.display.flip()
    clock.tick(60)
