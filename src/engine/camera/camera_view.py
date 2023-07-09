from __future__ import annotations
from typing import TYPE_CHECKING

# std import
import pygame
from pytmx import pytmx
import math

# nos propre fichier import
from engine.utils.settings import dev_settings
from engine.map.map_manager import MapManager
from debug import debug
from engine.utils.hitbox import RectangularHitbox
from engine.utils.enumerations import Side

# types hints
if TYPE_CHECKING:
    from engine.tower.tower_manager import TowerManager
    from engine.wave.wave_manager import WaveManager
class CameraView:
    """
    permet d'afficher une partie d'une map
    """
    def __init__(self, map_manager: MapManager, move_ease: float) -> None:

        self.map_manager = map_manager
        self.move_ease = move_ease
        self.factor = 1
        self.is_split = False

    def move(self, dt: float, teleport: bool=False) -> None:
        """
            Mettre a jour les coordonnés sur la map
        """
        ...

    def set_zoom(self, factor: float) -> None:
        # si le facteur de zoom a changé, on recalcul en fonction un zoom utilisable
        if self.factor != factor:
            map = self.map_manager.get_current_map()
            # on récupère un bon facteur
            self.factor = round(factor*map.tileheight)/map.tileheight

    def _tiles_to_draw(self, range_x: range, range_y: range, layer_index: int, animation_tiles: list, ticks: int, offset_x: int, offset_y: int, tilesize_factor: int) -> list:
        map = self.map_manager.get_current_map()
        tiles = []
        
        for x in range_x:
            for y in range_y:
                tile_image = map.get_tile_image(x, y, layer_index)
                if tile_image is not None:
                    gid = map.layers[layer_index].data[y][x]
                    if gid in animation_tiles:
                        animation_tile = animation_tiles[gid]
                        animation_time = ticks % animation_tile.total_time
                        animation_index = 0
                        animation_time_incremental = 0
                        while animation_time_incremental + animation_tile.frames[animation_index].duration < animation_time:
                            animation_time_incremental += animation_tile.frames[animation_index].duration
                            animation_index += 1

                        tile_image = map.images[animation_tile.frames[animation_index].gid]

                    posx = x * tilesize_factor + offset_x
                    posy = y * tilesize_factor + offset_y
                    
                    tiles.append((tile_image.get_image(self.factor), (posx, posy)))
        return tiles

    def _get_view_surface(self, coords: pygame.Vector2, width: int, height: int, tower_manager: TowerManager, wave_manager: WaveManager) -> pygame.Surface:

        draw_surface = pygame.Surface((width, height))

        map = self.map_manager.get_current_map()
        
        if map.background_color != None:
            draw_surface.fill(map.background_color)

        tile_size_factor = dev_settings.tile_size * self.factor

        half_width = width / 2
        half_height = height / 2

        x_const = half_width / (tile_size_factor)
        y_const = half_height / (tile_size_factor)

        offset_x = math.floor(- coords.x*tile_size_factor + half_width)
        offset_y = math.floor(- coords.y*tile_size_factor + half_height)
        offset = pygame.Vector2(offset_x,  offset_y)

        minx = max(math.floor(coords.x - x_const), 0)
        maxx = min(math.ceil(coords.x + x_const) + 1, map.width)

        miny = max(math.floor(coords.y - y_const), 0)
        maxy = min(math.ceil(coords.y + y_const) + 1, map.height)

        tiles = []
        animation_tiles = self.map_manager.animated_tiles[self.map_manager.current_map]
        ticks = pygame.time.get_ticks()
        
        for layer_index in range(len(map.layers)):
            if (isinstance(map.layers[layer_index], pytmx.TiledTileLayer)) and map.layers[layer_index].visible and map.layers[layer_index].name != "zone":
                tiles = self._tiles_to_draw(range(minx, maxx), range(miny, maxy), layer_index, animation_tiles, ticks, offset_x, offset_y, tile_size_factor)
                
                    
                draw_surface.fblits(tiles)
                
        wave_manager.draw(draw_surface)
        wave_manager.draw_ui(draw_surface)
        
        tower_manager.draw(draw_surface)
        tower_manager.draw_ui(draw_surface)
        
        return draw_surface, offset

    def draw(self, draw_surface: pygame.Surface, tower_manager: TowerManager, wave_manager: WaveManager) -> None:
        """
        permet d'afficher / de dessiner la map
        """

        map = self.map_manager.get_current_map()

        tile_size_factor = dev_settings.tile_size * self.factor

        
        
        center_pos = pygame.Vector2(map.width, map.height) // 2

        surface, offset = self._get_view_surface(center_pos, map.width*tile_size_factor, map.height*tile_size_factor, tower_manager, wave_manager)

        if map.background_color != None:
            draw_surface.fill(map.background_color)

        const_hardcore = pygame.Vector2(draw_surface.get_width(), draw_surface.get_height()) / 2 - center_pos * tile_size_factor
        draw_surface.blit(surface, const_hardcore)
        pygame.draw.rect(draw_surface, (255, 255, 255), (const_hardcore.x, const_hardcore.y, surface.get_width(), surface.get_height()), width=1)