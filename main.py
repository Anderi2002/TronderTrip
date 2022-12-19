from random import randint
import pygame as py
import numpy as np
import pickle
import json
from time import perf_counter
from threading import Thread
from destination import Destination # Is populated with info
from field import Field
from weather_scraper import get_weather

with open("data/destinations_info.json", "r") as file:
    destinations_info: dict[str: str | int] = json.load(file)

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


def update_temperature(name: str) -> None:
    get_weather(name, destinations_info)
    temperature = destinations_info[name]['temperature']
    temperature_field.data = temperature if temperature else ""


def next_destination(_destinations: list[Destination]) -> Destination:
    if not _destinations:
        _destinations[:] = destinations
    index = randint(0, len(_destinations) - 1)
    destination = _destinations[index]
    _destinations.pop(index)
    # Update fields
    elevation = destinations_info[destination.name]['elevation']
    elevation_field.data = int(elevation if elevation else 0)
    distance = destinations_info[destination.name]['distance']
    distance_field.data = int(distance if distance else 0) / 10 ** 3
    temperature_thread = Thread(target = update_temperature, args = (destination.name,))
    temperature_thread.start()
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
        temperature_field.draw(white)
        elevation_field.draw(white)
        distance_field.draw(white)
        py.display.update()


if __name__ == '__main__':
    main()


# TODO: Find geographic position
#   - Use google maps to estimate how long it will take
# TODO: Add buttons
#   - If accepted, it should send a message/mail with info regarding the trip