import pygame
import globals
import game.map
import engine.datahandler
import game.towers

from engine.ui import Panel, Image, Text, Button

def init():
    game.towers.setup()
    globals.current_map = game.map.Map(globals.MAP_TEST)

    globals.UI.append(
        Panel(800, 0, 200, 800, (
            engine.datahandler.colour_from_table(globals.json_assets["settings"]["ui"]["tower_bar_colour"])
        ), anchor='topleft')
    )

    game.towers.setup_ui()

def update_buttons(event=None):
    for ui in globals.UI:
        ui.update(event)

def process_event(event):
    game.towers.process_event(event)
    if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
        update_buttons(event)

def update():   
    globals.game_surface.fill((0,0,0))
    
    globals.current_map.update()

    game.towers.update()
    game.towers.draw(globals.game_surface)

    for ui in globals.UI:
        ui.render()
