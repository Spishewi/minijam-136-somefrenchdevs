from __future__ import annotations

# std import
import pytmx
import pygame
import math
#import numpy as np
from threading import Thread
import json
from collections import namedtuple

# nos propre fichier import
from engine.utils.image import DynamicImage
from engine.utils.enumerations import MemoryPriority
from engine.utils.settings import dev_settings
from engine.scene.scene_event import SCENE_SET_LOADINGSCREEN, SCENE_REMOVE_LOADINGSCREEN, SCENE_TRANSITION_OUT, scene_error_wrapper




MapTuple = namedtuple('MapTuple', ['priority', 'map'])

NEW_MAP_SET = pygame.event.custom_type()
"""
Must me triggered when an async map as been set
"""

class MapManager:
    def __init__(self, maps_json: str) -> None:
        self._maps = {}
        self._loading_maps = set()
        self._waiting_to_be_set = None
        self.animated_tiles = {}

        with open(maps_json) as f:
            self._maps_config = json.load(f)

        self.current_map = None
        self.current_tile_size = None

    def clear_memory(self):
        need_unload = []
        for map_name, map_tuple in self._maps.items():
            if map_name == self.current_map:
                continue
            elif map_tuple.priority == MemoryPriority.ALWAYS_UNLOAD:
                need_unload.append(map_name)
            elif map_tuple.priority == MemoryPriority.UNLOAD_IF_NEEDED and len(self._maps)-len(need_unload) > dev_settings.max_memory_map:
                need_unload.append(map_name)
        
        for map_name in need_unload:
            self.unload(map_name)


    def unload(self, map_name) -> None:
        del self._maps[map_name]
    
    def set_map(self, map_name: str, auto_load=False) -> None:
        self.new_map_name = map_name
        if map_name not in self._maps.keys():
            if auto_load:
                self.load_map_async(map_name)
                self._waiting_to_be_set = map_name
                return
            else:
                raise ValueError(f"{map_name} is not loaded !")
            
        
        
        
        pygame.event.post(pygame.Event(SCENE_TRANSITION_OUT))
        pygame.event.post(pygame.Event(NEW_MAP_SET))
    
    def load_map_async(self, map_name: str) -> None:
        if map_name in self._maps.keys():
            raise ValueError(f"{map_name} is already loaded !")

        if map_name in self._loading_maps:
            raise ValueError(f"{map_name} is already trying to be loaded !")
        
        thread = Thread(target=scene_error_wrapper, args=(self.load_map, map_name))
        thread.start()

    def load_map(self, map_name: str) -> None:
        """
        Permet d'ajouter une map au gestionnaire
        """
        pygame.event.post(pygame.Event(SCENE_SET_LOADINGSCREEN))

        # On l'ajoute à la liste des maps en cours de chargement
        self._loading_maps.add(map_name)

        # On crée la map
        new_map = pytmx.TiledMap(self._maps_config[map_name]["path"], image_loader=DynamicImage.image_loader)

        # On vérifie qu'elle est compatible
        if dev_settings.tile_size != new_map.tilewidth:
            raise ValueError(f"""{map_name} is not compatible\nwrong tile size !""")


        # On charge les animations
        animated_tiles = {}

        for gid, props in new_map.tile_properties.items():

            # iterate over the frames of the animation
            # if there is no animation, this list will be empty
            frames = []
            for animation_frame in props['frames']:
                frames.append(animation_frame)
            if frames != []:
                animated_tiles[gid] = AnimatedTile(frames, sum([i.duration for i in frames]))

        self._maps[map_name] = MapTuple(self._maps_config[map_name]["priority"], new_map)
        self.animated_tiles[map_name] = animated_tiles

        self._loading_maps.remove(map_name)
        pygame.event.post(pygame.Event(SCENE_REMOVE_LOADINGSCREEN))

        
    
    def get_map(self, map_name: str) -> pytmx.TiledMap:
        return self._maps[map_name].map

    def get_current_map(self) -> pytmx.TiledMap:
        return self.get_map(self.current_map)

    def get_around_collisions(self, map_name: str, coords: pygame.Vector2, size: int, layers_names: list[str], reverse:bool = False) -> dict[str,list[pygame.Vector2]]:
        map = self.get_map(map_name)

        minx = max(0, math.floor(coords.x) - size)
        maxx = min(map.width, math.ceil(coords.x) + size)
        miny = max(0, math.floor(coords.y) - size)
        maxy = min(map.height, math.ceil(coords.y) + size)
        
        # pareil les discitonnaires sont pas opti comme structure, faudrait trouver autre chose
        around_collisions = {}
        for layer_name in layers_names:
            layer = map.get_layer_by_name(layer_name)
            
            # append est gourmande comme fonction, donc j'ai écrit comme ça, ça devrait être plus opti
            # ça fait la même chose
            # techiniquement je pourrais même utiliser les dictionnaires en comprehension, mais pour deux/3 tours de boucle,
            # on perdrais en lisibilité pour pas grand chose
            if not reverse:
                tiles = [pygame.Vector2(x, y) for x in range(minx, maxx) for y in range(miny, maxy) if layer.data[y][x] != 0]
            else:
                tiles = [pygame.Vector2(x, y) for x in range(minx, maxx) for y in range(miny, maxy) if layer.data[y][x] == 0]
            around_collisions[layer_name] = tiles
        return around_collisions
    
    def update(self) -> None:
        if self._waiting_to_be_set != None and self._waiting_to_be_set in self._maps.keys():
            self.set_map(self._waiting_to_be_set)
            self._waiting_to_be_set = None


class AnimatedTile:
    def __init__(self, frames: list, total_time: int) -> None:
        self.frames = frames
        self.total_time = total_time