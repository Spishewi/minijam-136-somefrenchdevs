from __future__ import annotations
import pytmx
import pygame
import math
from pathlib import Path
#import numpy as np

class DynamicImage:
    """
    Une classe qui permet à une image de s'occuper individuellement de sa propre taille / niveau de zoom.
    """
    def __init__(self, image: pygame.Surface, smooth: bool=False) -> None:
        self._original_image = image
        self._resized_image = image
        self._current_factor = 1

        self._original_image_width = self._original_image.get_width()
        self._original_image_height = self._original_image.get_height()

        self._smooth = smooth

        """
        pixels_alpha_array = pygame.surfarray.pixels_alpha(self._original_image).flatten()

        self.opaque = True
        for pixel in pixels_alpha_array:
            if pixel == 0:
                self.opaque = False
                #pygame.draw.rect(self._original_image, (127, 255, 127), (6, 6, 4, 4))
                break
        """
        

    def get_image(self, factor: float) -> pygame.Surface:
        """
        Permet récupérer l'image de bonne taille en fonction d'un facteur.
        L'image est si besoin redimentionné, et mise en cache.
        """
        if factor <= 0:
            raise ValueError("factor must be > 0")

        if factor != self._current_factor:
            self._current_factor = factor
            new_size = (math.floor(self._original_image_width*factor), math.floor(self._original_image_height*factor))
            if self._smooth:
                self._resized_image = pygame.transform.smoothscale(self._original_image, size=new_size)
            else:
                self._resized_image = pygame.transform.scale(self._original_image, size=new_size)
            #self._resized_image = self._resized_image.convert_alpha()
        return self._resized_image

    @staticmethod
    def image_loader(file_path: Path, colorkey=None, **kwargs):
        """
        pytmx.TiledMap() utilise cette fonction pour charger toutes ses images.
        """

        tileset_image = pygame.image.load(file_path)
        tileset_image = tileset_image.convert_alpha()
        tileset_image.set_colorkey(colorkey)

        def extract_image(rect: tuple, flags: pytmx.TileFlags) -> DynamicImage:
            tile_size = rect[2]
            tile_surface = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
            tile_surface.blit(tileset_image, (0, 0), rect)
            #tile_surface = tile_surface.convert_alpha()
            return DynamicImage(tile_surface, smooth=False)
        return extract_image