import game.map
import globals

def init():
    globals.current_map = game.map.Map(globals.MAP_TEST)

def update():
    globals.current_map.update()