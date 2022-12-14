from destination import Destination # Is populated with info
from random import randint
import pygame as py
import numpy as np
import pickle
from field import Field

# Import data of each destination
with open("data/destinations.pickle", "rb") as file:
    destinations: list[Destination] = pickle.load(file)

# Initiate pygame
py.init()
screen = py.display.set_mode((2560, 1440))
screen_size = screen.get_size() # For scaling to different screens
py.display.set_caption("Trondertrip")
trondertip_icon = py.image.load("icons/trondertrip_icon.png")
py.display.set_icon(trondertip_icon)
print(screen_size)

# Colors
grey = (40, 40, 40)
black = (0, 0, 0)
white = (230, 230, 230)

# Fonts
header = lambda n: py.font.Font('freesansbold.ttf', n)

# Fields
temperature_field = Field(screen, 100, 300, header(64), "icons/temperature.png", "°C")
elevation_field = Field(screen, 100, 500, header(64), "icons/snowed-mountains.png", "m")
distance_field = Field(screen, 100, 700, header(64), "icons/path.png", "km")

def draw_text(destination: Destination, pos: list[int, int], font: py.font.Font, color = black) -> None:
    text = font.render(destination.name, True, color)
    textRect = text.get_rect()
    textRect.width += 10
    textRect.height += 10
    textRect.center = pos
    py.draw.rect(screen, white, textRect, border_radius = 20)
    textRect = text.get_rect()
    textRect.center = pos
    screen.blit(text, textRect)


def draw_image(destination: Destination, pos: tuple[int, int], scale: float) -> None:
    imp = py.image.load(f"images/{destination.name}.jpg")
    image_rect = imp.get_rect()
    imp = py.transform.scale(imp, (np.array(image_rect.bottomright) * screen_size[0] * scale / image_rect.bottomright[0]).astype(int))
    image_rect = imp.get_rect()
    image_rect.center = pos
    screen.blit(imp, image_rect)


def float_to_coords(x: float, y: float) -> tuple[int, int]:
    return [int(screen_size[0] * x), int(screen_size[1] * y)]


def next_destination(_destinations: list[Destination]) -> Destination:
    if not _destinations:
        _destinations[:] = destinations
    index = randint(0, len(_destinations) - 1)
    destination = _destinations[index]
    _destinations.pop(index)
    return destination


def main():
    remaining_destinations = list(destinations)
    destination = next_destination(remaining_destinations)
    running = True
    while running:
        screen.fill(grey)
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False
            if event.type == py.KEYUP:
                if event.key == py.K_ESCAPE:
                    running = False
                elif event.key == py.K_RETURN:
                    destination = next_destination(remaining_destinations)
        draw_image(destination, float_to_coords(0.7, 0.5), 0.5)
        draw_text(destination, float_to_coords(0.5, 0.1), header(128))
        temperature_field.draw(-10, white)
        elevation_field.draw(128, white)
        distance_field.draw(1.75, white)
        py.display.update()


if __name__ == '__main__':
    main()


# TODO: Find geographic position
#   - Use google maps to estimate how long it will take
# TODO: Show temperature in that area
# TODO: Add buttons
#   - If accepted, it should send a message/mail with info regarding the trip