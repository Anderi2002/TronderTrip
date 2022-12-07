import pygame as py
import copy

class Field:
    curvature = 20
    black = (0, 0, 0)
    x_offset = 10
    y_offset = 10
    spacing = 10
    icon_scale = 2

    def __init__(self, screen: py.display, x_pos: int, y_pos: int, font: py.font.Font, icon_link: str, unit: str) -> None:
        self.screen = screen
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.font: py.font.Font = font
        self.icon = py.image.load(icon_link)
        self.unit = unit

        self.data = -1

        self.text = font.render(self.unit, True, self.black)
        self.box = self.text.get_rect()
        self.icon = py.transform.scale(self.icon, \
            (int(self.icon.get_size()[0] * self.box.height / (self.icon.get_size()[1]) * self.icon_scale), \
                self.icon_scale * self.box.height))
    
    def draw(self, data: int | float, background_color: tuple[int, ...]):
        if data != self.data:
            self.data = data
            self.text = self.font.render(f"{data} {self.unit}", True, self.black)
            text_box: py.rect.Rect = self.text.get_rect()
            self.box = py.Rect(self.x_pos, self.y_pos, 2 * self.x_offset + \
                self.icon.get_size()[0] + self.spacing + text_box.width, 2 * self.y_offset + self.icon.get_size()[1])
        # Draws background
        py.draw.rect(self.screen, background_color, self.box, border_radius = self.curvature)
        box_copy = copy.copy(self.box)
        box_copy.top += self.y_offset
        box_copy.left += self.x_offset
        # Draw icon
        self.screen.blit(self.icon, box_copy)
        box_copy.left += self.icon.get_size()[0] + self.spacing
        box_copy.top += int(self.icon.get_size()[1] / 4)
        # Draw text
        self.screen.blit(self.text, box_copy)
