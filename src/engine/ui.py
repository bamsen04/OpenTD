import pygame
import globals

class UiBase:
    def __init__(self, ui_id=None, anchor='topleft'):
        # anchor can be 'topleft', 'topright', 'bottomleft', 'bottomright', 'center'
        self.ui_id = ui_id
        self.anchor = anchor
        if ui_id is not None:
            globals.UI.append(self)

    def update(self, event=None):
        raise NotImplementedError("Subclasses must implement this method")

    def render(self):
        raise NotImplementedError("Subclasses must implement this method")

    def destroy(self):
        if self in globals.UI:
            globals.UI.remove(self)

    def _get_position(self, width, height):
        # Returns actual (x,y) based on anchor and stored self.x, self.y
        if self.anchor == 'topleft':
            return self.x, self.y
        elif self.anchor == 'topright':
            return self.x - width, self.y
        elif self.anchor == 'bottomleft':
            return self.x, self.y - height
        elif self.anchor == 'bottomright':
            return self.x - width, self.y - height
        elif self.anchor == 'center':
            return self.x - width // 2, self.y - height // 2
        else:
            return self.x, self.y  # fallback

class Panel(UiBase):
    def __init__(self, x, y, sizex, sizey, background_color, ui_id=None, anchor='topleft'):
        super().__init__(ui_id, anchor)
        self.x, self.y = x, y
        self.sizex, self.sizey = sizex, sizey
        self.background_color = background_color

    def update(self, event=None):
        pass

    def render(self):
        pos = self._get_position(self.sizex, self.sizey)
        pygame.draw.rect(globals.game_surface, self.background_color, (*pos, self.sizex, self.sizey))

class Image(UiBase):
    def __init__(self, x, y, image, sizex, sizey, ui_id=None, anchor='topleft'):
        super().__init__(ui_id, anchor)
        self.x, self.y = x, y
        self.image = image
        self.sizex, self.sizey = sizex, sizey
        self.scaled_image = pygame.transform.scale(self.image, (self.sizex, self.sizey))

    def update(self, event=None):
        pass

    def render(self):
        pos = self._get_position(self.sizex, self.sizey)
        globals.game_surface.blit(self.scaled_image, pos)

class Text(UiBase):
    def __init__(self, x, y, sizex, sizey, text, font_size, font_scale_auto, text_align, text_colour, ui_id=None, anchor='topleft'):
        super().__init__(ui_id, anchor)
        self.x, self.y = x, y
        self.sizex, self.sizey = sizex, sizey
        self.text = text
        self.font_size = font_size
        self.font_scale_auto = font_scale_auto
        self.text_align = text_align
        self.text_colour = text_colour
        self.font = pygame.font.SysFont(None, self.font_size)

    def update(self, event=None):
        pass

    def render(self):
        pos = self._get_position(self.sizex, self.sizey)
        rendered_text = self.font.render(self.text, True, self.text_colour)
        text_rect = rendered_text.get_rect()

        # Position text_rect relative to pos and text_align inside box (sizex, sizey)
        if self.text_align == 'center':
            text_rect.center = (pos[0] + self.sizex // 2, pos[1] + self.sizey // 2)
        elif self.text_align == 'left':
            text_rect.midleft = (pos[0] + 5, pos[1] + self.sizey // 2)
        elif self.text_align == 'right':
            text_rect.midright = (pos[0] + self.sizex - 5, pos[1] + self.sizey // 2)
        else:
            text_rect.topleft = pos

        globals.game_surface.blit(rendered_text, text_rect)

class Button(Panel):
    def __init__(self, x, y, sizex, sizey, text, font_size, font_scale_auto, text_align, text_colour, background_colour, onclick, ui_id=None, anchor='topleft'):
        super().__init__(x, y, sizex, sizey, background_colour, ui_id, anchor)
        self.text = text
        self.font_size = font_size
        self.font_scale_auto = font_scale_auto
        self.text_align = text_align
        self.text_colour = text_colour
        self.onclick = onclick
        self.hovered = False
        self.pressed = False
        self.font = pygame.font.SysFont(None, self.font_size)

    def update(self, event=None):
        if event is None:
            return

        if 'pos' not in event or 'type' not in event:
            return

        x, y = event['pos']
        pos = self._get_position(self.sizex, self.sizey)
        inside = pos[0] <= x <= pos[0] + self.sizex and pos[1] <= y <= pos[1] + self.sizey

        if event['type'] == 'MOUSEMOTION':
            self.hovered = inside
        elif event['type'] == 'MOUSEBUTTONDOWN' and inside:
            self.pressed = True
        elif event['type'] == 'MOUSEBUTTONUP':
            if self.pressed and inside and self.onclick:
                self.onclick()
            self.pressed = False

    def render(self):
        pos = self._get_position(self.sizex, self.sizey)

        bg_color = self.background_color
        if self.pressed:
            bg_color = tuple(min(255, c + 40) for c in self.background_color)
        elif self.hovered:
            bg_color = tuple(min(255, c + 20) for c in self.background_color)

        pygame.draw.rect(globals.game_surface, bg_color, (*pos, self.sizex, self.sizey))

        rendered_text = self.font.render(self.text, True, self.text_colour)
        text_rect = rendered_text.get_rect()

        if self.text_align == 'center':
            text_rect.center = (pos[0] + self.sizex // 2, pos[1] + self.sizey // 2)
        elif self.text_align == 'left':
            text_rect.midleft = (pos[0] + 5, pos[1] + self.sizey // 2)
        elif self.text_align == 'right':
            text_rect.midright = (pos[0] + self.sizex - 5, pos[1] + self.sizey // 2)
        else:
            text_rect.topleft = pos

        globals.game_surface.blit(rendered_text, text_rect)
