import pygame
import globals
from util import window_to_game_coords

class UiBase:
    def __init__(self, ui_id=None, anchor='topleft'):
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
            return self.x, self.y

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
        self.font = pygame.font.Font("font", self.font_size)
        self.lines = []

    def _wrap_text(self, font, text, max_width):
        words = text.split(' ')
        lines = []
        current_line = ''
        for word in words:
            test_line = current_line + ('' if current_line == '' else ' ') + word
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line != '':
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines

    def _auto_scale_font(self):
        font_size = 4
        max_font_size = self.font_size
        best_font = None
        best_lines = None

        while font_size <= max_font_size:
            font = pygame.font.Font("font", font_size)
            lines = self._wrap_text(font, self.text, self.sizex)
            line_height = font.get_linesize()
            max_line_width = max(font.size(line)[0] for line in lines) if lines else 0
            total_height = line_height * len(lines)

            if total_height > self.sizey or max_line_width > self.sizex:
                break

            best_font = font
            best_lines = lines
            font_size += 1

        if best_font is not None:
            self.font = best_font
            self.lines = best_lines
        else:
            self.font = pygame.font.Font("font", 4)
            self.lines = self._wrap_text(self.font, self.text, self.sizex)

    def update(self, event=None):
        pass

    def render(self):
        pos = self._get_position(self.sizex, self.sizey)
        if self.font_scale_auto:
            self._auto_scale_font()
        else:
            self.lines = self._wrap_text(self.font, self.text, self.sizex)

        line_height = self.font.get_linesize()
        total_text_height = line_height * len(self.lines)

        y_start = pos[1]
        if self.text_align == 'center':
            y_start = pos[1] + (self.sizey - total_text_height) // 2

        for i, line in enumerate(self.lines):
            rendered_text = self.font.render(line, True, self.text_colour)
            text_rect = rendered_text.get_rect()

            if self.text_align == 'center':
                text_rect.centerx = pos[0] + self.sizex // 2
            elif self.text_align == 'left':
                text_rect.x = pos[0] + 5
            elif self.text_align == 'right':
                text_rect.right = pos[0] + self.sizex - 5
            else:
                text_rect.x = pos[0]

            text_rect.y = y_start + i * line_height

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
        self.font = pygame.font.Font("font", self.font_size)
        self.lines = []

    def _wrap_text(self, font, text, max_width):
        words = text.split(' ')
        lines = []
        current_line = ''
        for word in words:
            test_line = current_line + ('' if current_line == '' else ' ') + word
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line != '':
                    lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines

    def _auto_scale_font(self):
        font_size = 4
        max_font_size = self.font_size
        best_font = None
        best_lines = None

        while font_size <= max_font_size:
            font = pygame.font.Font("font", font_size)
            lines = self._wrap_text(font, self.text, self.sizex - 10)
            line_height = font.get_linesize()
            max_line_width = max(font.size(line)[0] for line in lines) if lines else 0
            total_height = line_height * len(lines)

            if total_height > self.sizey - 10 or max_line_width > self.sizex - 10:
                break

            best_font = font
            best_lines = lines
            font_size += 1

        if best_font is not None:
            self.font = best_font
            self.lines = best_lines
        else:
            self.font = pygame.font.Font("font", 4)
            self.lines = self._wrap_text(self.font, self.text, self.sizex - 10)

    def update(self, event=None):
        if event is None or not hasattr(event, 'pos') or not hasattr(event, 'type'):
            return

        window_size = pygame.display.get_window_size()
        mouse_pos = window_to_game_coords(event.pos, window_size)

        pos = self._get_position(self.sizex, self.sizey)
        rect = pygame.Rect(pos[0], pos[1], self.sizex, self.sizey)
        inside = rect.collidepoint(mouse_pos)

        if event.type == pygame.MOUSEMOTION:
            self.hovered = inside
        elif event.type == pygame.MOUSEBUTTONDOWN and inside:
            self.pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
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

        if self.font_scale_auto:
            self._auto_scale_font()
        else:
            self.lines = self._wrap_text(self.font, self.text, self.sizex - 10)

        line_height = self.font.get_linesize()
        total_text_height = line_height * len(self.lines)

        y_start = pos[1] + (self.sizey - total_text_height) // 2

        for i, line in enumerate(self.lines):
            rendered_text = self.font.render(line, True, self.text_colour)
            text_rect = rendered_text.get_rect()

            if self.text_align == 'center':
                text_rect.centerx = pos[0] + self.sizex // 2
            elif self.text_align == 'left':
                text_rect.x = pos[0] + 5
            elif self.text_align == 'right':
                text_rect.right = pos[0] + self.sizex - 5
            else:
                text_rect.x = pos[0] + 5

            text_rect.y = y_start + i * line_height

            globals.game_surface.blit(rendered_text, text_rect)
