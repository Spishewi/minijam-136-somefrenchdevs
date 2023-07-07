from __future__ import annotations
import pygame
import math
import random

from engine.utils.hitbox import Hitbox, CircularHitbox
from pytmx import pytmx

from engine.utils.settings import dev_settings
from engine.utils.color import tiled_hex_to_rgb

from objects.game_object import GameObject

class Light(GameObject):
    original_image: pygame.Surface | None = None
    lights_surface: dict[tuple[int, pygame.Color], pygame.Surface] = {}

    def __init__(self, center: pygame.Vector2, strength: float, color: pygame.Color, light_min: float, light_max: float) -> None:

        self._center = center
        self._strength = strength
        self._color = color

        self._light_min = light_min
        self._light_max = light_max

        self._light_surface = Light.get_light_surface(self._strength, self._color)

    def get_pos(self) -> pygame.Vector2:
        return self._center - pygame.Vector2(self._strength/2, self._strength/2)

    def get_center(self) -> pygame.Vector2:
        return self._center

    def get_hitbox(self) -> Hitbox:
        return CircularHitbox(self._center, self._strength)
    
    def set_center(self, pos: pygame.Vector2) -> None:
        self._center = pos

    def draw_ui(self, draw_surface: pygame.Surface, offset: pygame.Vector2, factor: float, **kwargs) -> None:
        luminance = int(((math.sin(self.get_pos().x / 5 - pygame.time.get_ticks() / 1000)+1) / 2 * (self._light_max-self._light_min) + self._light_min) * 255)

        light_surface = pygame.Surface(self._light_surface.get_size())
        light_surface.fill(pygame.Color(luminance, luminance, luminance))
        light_surface.blit(self._light_surface, (0, 0), special_flags=pygame.BLEND_MULT)

        draw_surface.blit(light_surface, self.get_pos() * dev_settings.tile_size + offset, special_flags=pygame.BLEND_ADD)
    
    @staticmethod
    def get_light_surface(strength: float, color: pygame.Color) -> pygame.Surface:
        if Light.original_image == None:
            Light.original_image = pygame.image.load("../assets/light/gradient.png").convert()

        strength_size = strength * dev_settings.tile_size
        surface_size = pygame.Vector2(strength_size, strength_size)

        if (strength, str(color)) in Light.lights_surface.keys():
            colored_light = Light.lights_surface[strength, str(color)]
        else:
            white_light = pygame.transform.smoothscale(Light.original_image, surface_size)

            colored_light = pygame.Surface(surface_size)
            colored_light.fill(color)
            colored_light.blit(white_light, (0, 0), special_flags=pygame.BLEND_MULT)

            Light.lights_surface[strength, str(color)] = colored_light

        return colored_light


    @staticmethod
    def loader(light_gid: int, properties: dict, map: pytmx.TiledMap) -> list[Light]:
        objects = []

        strength = properties["light_strength"]
        color = tiled_hex_to_rgb(properties["light_color"])
        color = pygame.Color(color)
        light_min = properties["light_min"]
        light_max = properties["light_max"]

        for layer in map.layers:
            if (isinstance(layer, pytmx.TiledTileLayer)) and layer.visible:
                for x in range(map.width):
                    for y in range(map.height):
                        gid = layer.data[y][x]
                        if gid == light_gid:
                            objects.append(Light(pygame.Vector2(x+1/2, y+1/2), strength, color, light_min, light_max))

        return objects
    