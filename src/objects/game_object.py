from __future__ import annotations
import pygame

from engine.utils.hitbox import Hitbox
from pytmx import pytmx

class GameObject:
    def get_pos(self) -> pygame.Vector2:
        pass

    def get_center(self) -> pygame.Vector2:
        pass

    def get_hitbox(self) -> Hitbox:
        pass

    def draw(self, draw_surface: pygame.Surface, offset: pygame.Vector2, factor: float, **kwargs) -> None:
        pass

    def draw_ui(self, draw_surface: pygame.Surface, **kwargs) -> None:
        pass

    def update(self, dt: float, **kwargs):
        pass

    def event_handler(self, event: pygame.Event, **kwargs) -> None:
        pass

    @staticmethod
    def loader(tiled_object: pytmx.TiledObject) -> GameObject:
        pass