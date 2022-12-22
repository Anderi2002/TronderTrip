
import pygame as py
from pygame import gfxdraw
from math import sqrt
from destination import Destination
from typing import Callable 
import numpy as np
from threading import Thread


class Button:
    white = (255, 255, 255)
    black = (0, 0, 0)

    def __init__(self, screen: py.Surface, coords: tuple[int, int], color: tuple[int, int, int], radius: int, method: Callable[[Destination, dict[str: str | int]], None], icon: str) -> None:
        self.screen = screen
        self.x, self.y = coords
        self.color = color
        self.method = method
        self.radius = int(self.screen.get_size()[0] / 1000 * radius)
        self.icon = py.image.load(icon)
        self.icon = py.transform.scale(self.icon, (np.array([2 * self.radius, 2 * self.radius]) * 0.7).astype(int))
        self.rect = self.icon.get_rect()
        self.rect.center = coords

        self.border = self.black
    

    def is_cursor_on_button(self, coords: tuple[int, int]) -> bool:
        if sqrt((coords[0] - self.x) ** 2 + (coords[1] - self.y) ** 2) < self.radius:
            return True
        else:
            return False
    

    def draw(self, mouse_pos: tuple[int, int]) -> None:
        if self.is_cursor_on_button(mouse_pos):
            self.border = self.white
        else:
            self.border = self.black
        gfxdraw.filled_circle(self.screen, self.x, self.y, self.radius, self.color)
        gfxdraw.aacircle(self.screen, self.x, self.y, self.radius, self.border)
        # Icon
        self.screen.blit(self.icon, self.rect)

    
    def button_press(self, mouse_pos: tuple[int, int], destination: Destination, destinations_info: dict[str: str | int]) -> None:
        if self.is_cursor_on_button(mouse_pos):
            thread = Thread(target = self.method, args = (destination, destinations_info))
            thread.start()
