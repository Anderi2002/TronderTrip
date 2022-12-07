from destination import Destination # Is populated with info
from random import randint
import pygame as py
import numpy as np
from yr.libyr import Yr # Api for yr
import pickle

# Import data of each destination
with open("data/destinations.pickle", "rb") as file:
    destinations: list[Destination] = pickle.load(file)

# Initiate pygame
py.init()
screen = py.display.set_mode((0, 0), py.FULLSCREEN)
screen_size = screen.get_size() # For scaling to different screens
py.display.set_caption("Destination Finder")

# Colors
black = (0, 0, 0)
white = (230, 230, 230)

# Fonts
header = lambda n: py.font.Font('freesansbold.ttf', n)


def draw_text(destination: Destination, pos: tuple[int, int], font: py.font.Font, color = white) -> None:
    text = font.render(destination.name, True, color, black)
    textRect = text.get_rect()
    textRect.center = pos
    screen.blit(text, textRect)
    py.draw.rect(screen, white, textRect, 5)


def draw_image(destination: Destination, pos: tuple[int, int], scale: float) -> None:
    imp = py.image.load(f"images/{destination.name}.jpg")
    image_rect = imp.get_rect()
    imp = py.transform.scale(imp, (np.array(image_rect.bottomright) * screen_size[0] * scale / image_rect.bottomright[0]).astype(int))
    image_rect = imp.get_rect()
    image_rect.center = pos
    screen.blit(imp, image_rect)


def float_to_coords(x: float, y: float) -> tuple[int, int]:
    return (int(screen_size[0] * x), int(screen_size[1] * y))


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
        screen.fill(black)
        for event in py.event.get():
            if event.type == py.KEYUP:
                if event.key == py.K_ESCAPE:
                    running = False
                elif event.key == py.K_RETURN:
                    destination = next_destination(remaining_destinations)
        draw_image(destination, float_to_coords(0.7, 0.5), 0.5)
        draw_text(destination, float_to_coords(0.5, 0.1), header(128))
        py.display.update()


if __name__ == '__main__':
    main()


# TODO: Find geographic position
#   - Use google maps to estimate how long it will take
# TODO: Show temperature in that area
# TODO: Add buttons
#   - If accepted, it should send a message/mail with info regarding the trip