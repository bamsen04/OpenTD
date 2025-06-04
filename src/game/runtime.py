import pygame
import globals
import game.map
import engine.datahandler

from engine.ui import Panel, Image, Text, Button

def init():
    globals.current_map = game.map.Map(globals.MAP_TEST)

    globals.UI.append(
        Panel(800, 0, 200, 800, (
            engine.datahandler.colour_from_table(globals.json_assets["settings"]["ui"]["tower_bar_colour"])
        ), anchor='topleft')
    )

def update_buttons(event=None):
    for ui in globals.UI:
        ui.update(event)

def process_event(event):
    if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
        event_dict = {'type': pygame.event.event_name(event.type), 'pos': event.pos}
        update_buttons(event_dict)
    else:
        update_buttons()

def update():   
    globals.game_surface.fill((0,0,0))
    
    globals.current_map.update()

    for ui in globals.UI:
        ui.render()
