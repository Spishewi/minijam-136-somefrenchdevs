from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
from pytmx import pytmx

from objects.game_object import GameObject
from engine.utils.hitbox import RectangularHitbox
from engine.utils.settings import dev_settings
from engine.utils.quadtree import QuadTree

from objects.light import Light

if TYPE_CHECKING:
    from engine.map.map_manager import MapManager

from debug import debug

class ObjectsManager():
    def __init__(self, map: pytmx.TiledMap, **kwargs) -> None:

        self._map = map
        quadtree_hitbox = RectangularHitbox(pygame.Vector2(0, 0), map.width/dev_settings.tile_size, map.height/dev_settings.tile_size)
        self._objects = QuadTree(quadtree_hitbox)
        self._load(**kwargs)

    def _load(self, **kwargs):
        self._objects = QuadTree(self._objects.boundary)
        
        for game_object in self._map.objects:
            ...
            
        for gid, properties in self._map.tile_properties.items():
            if "light_strength" in properties:
                self._objects.extend(Light.loader(gid, properties, self._map))

    def draw(self, draw_surface: pygame.Surface, offset: pygame.Vector2,  **kwargs) -> None:
        surface_hitbox = RectangularHitbox(-offset / dev_settings.tile_size, draw_surface.get_width() / dev_settings.tile_size, draw_surface.get_height() / dev_settings.tile_size)
        objects_to_draw = self._objects.query(surface_hitbox)
        for current_place, game_object in objects_to_draw:
            game_object.draw(draw_surface, offset, **kwargs)

    def draw_ui(self, draw_surface: pygame.Surface, offset: pygame.Vector2,  **kwargs) -> None:
        surface_hitbox = RectangularHitbox(-offset / dev_settings.tile_size, draw_surface.get_width() / dev_settings.tile_size, draw_surface.get_height() / dev_settings.tile_size)
        objects_to_draw = self._objects.query(surface_hitbox)
        for current_place, game_object in objects_to_draw:
                game_object.draw_ui(draw_surface, offset=offset, **kwargs)

    def update(self, dt: float, **kwargs) -> None:
        i = 0
        for current_place, game_object in self._objects.all():
            game_object.update(dt, **kwargs)
            obj_hitbox = game_object.get_hitbox()
            if obj_hitbox != current_place:
                self._objects.update(current_place, game_object)
            i+=1
        

    def event_handler(self, event: pygame.Event, **kwargs) -> None:
        for current_place, game_object in self._objects.all():
            game_object.event_handler(event, **kwargs)