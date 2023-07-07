from __future__ import annotations
from typing import TYPE_CHECKING
import pygame

from objects.game_object import GameObject

if TYPE_CHECKING:
    from engine.map.map_manager import MapManager

class Entity(GameObject):
    def teleport(self, position: pygame.Vector2) -> None:
        pass

    def move(self, dt: float, map_manager: MapManager) -> None:
        pass