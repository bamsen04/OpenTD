import globals
import pygame

def window_to_game_coords(mouse_pos, window_size):
    wx, wy = mouse_pos
    ww, wh = window_size
    vw, vh = globals.VIEWABLE_WIDTH, globals.VIEWABLE_HEIGHT
    view_aspect = vw / vh
    window_aspect = ww / wh

    if window_aspect > view_aspect:
        # Window wider than viewable area: letterbox vertical
        scaled_height = wh
        scaled_width = int(wh * view_aspect)
        offset_x = (ww - scaled_width) // 2
        game_x = (wx - offset_x) * (vw / scaled_width)
        game_y = wy * (vh / scaled_height)
    else:
        # Window taller than viewable area: letterbox horizontal
        scaled_width = ww
        scaled_height = int(ww / view_aspect)
        offset_y = (wh - scaled_height) // 2
        game_x = wx * (vw / scaled_width)
        game_y = (wy - offset_y) * (vh / scaled_height)

    return int(game_x), int(game_y)

def window_to_game_coords_auto(mouse_pos):
    window_size = pygame.display.get_window_size()
    return window_to_game_coords(mouse_pos, window_size)
