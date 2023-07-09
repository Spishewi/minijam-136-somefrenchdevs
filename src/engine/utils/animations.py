from __future__ import annotations
from typing import TYPE_CHECKING

import pygame, random

from engine.utils.image import DynamicImage
from engine.utils.enumerations import Gravity
from engine.utils.settings import Settings

if TYPE_CHECKING:
    from engine.wave.enemies.skeleton import Skeleton
    
class Animation:
    """
    gère les animations du joueur
    """
    def __init__(self, path: str) -> None:
        spritesheet = pygame.image.load(path + "/image.png").convert_alpha()
        self.settings = Settings.from_file_path(path + "/keyframes.json")
        
        self.sprites = self.load_sprites(spritesheet)

    def load_sprites(self, spritesheet: pygame.Surface, _load_settings: Settings | None = None) -> Sprite:
        """
        charge les sprites à partir d'un dictionnaire
        """
        if _load_settings == None :
            _load_settings = self.settings.keyframes
        sprites = Sprite()
        for k,v in _load_settings.to_dict().items():
            if type(v) == dict:
                setattr(sprites, k, self.load_sprites(spritesheet, Settings(v)))
            elif v[0] == v[1]:
                rect = (v[0][0] * self.settings.sprite_width, v[0][1] * self.settings.sprite_height, self.settings.sprite_width, self.settings.sprite_height)
                tile_surface = pygame.Surface((self.settings.sprite_width, self.settings.sprite_height), pygame.SRCALPHA)
                tile_surface.blit(spritesheet, (0, 0), rect)
                setattr(sprites, k, DynamicImage(tile_surface))
            else:
                sprite_list = []
                for x in range(v[0][0], v[1][0]+1):
                    for y in range(v[0][1], v[1][1]+1):
                        rect = (x * self.settings.sprite_width, y * self.settings.sprite_height, self.settings.sprite_width, self.settings.sprite_height)
                        tile_surface = pygame.Surface((self.settings.sprite_width, self.settings.sprite_height), pygame.SRCALPHA)
                        tile_surface.blit(spritesheet, (0, 0), rect)
                        sprite_list.append(DynamicImage(tile_surface))
                setattr(sprites, k, sprite_list)

        return sprites
    


class EnemyAnimation(Animation):
    def __init__(self, path: str) -> None:
        Animation.__init__(self, path)
        self.time_offset = random.randint(0, 1000)
        
    def get_curent_animation(self, velocity: pygame.Vector2()) -> pygame.Surface:     
        """
        renvoie une surface pygame contenant l'image du joueur
        cette image est choisie en fonction des mouvements du joueur
        """       
        img_id = (pygame.time.get_ticks() + self.time_offset) // 250 % 2
        
        # grappiné
        if velocity.x > 0:
            return self.sprites.right[img_id].get_image(1)
        elif velocity.x < 0:
            return self.sprites.left[img_id].get_image(1)
        elif velocity.y > 0:
            return self.sprites.down[img_id].get_image(1)
        else:
            return self.sprites.up[img_id].get_image(1)
        
class FieldAnimation(Animation):
    def __init__(self, path: str) -> None:
        Animation.__init__(self, path)
        self.time_offset = random.randint(0, 1000)
        
    def get_curent_animation(self, img_id: int) -> pygame.Surface:     
        """
        renvoie une surface pygame contenant l'image du joueur
        cette image est choisie en fonction des mouvements du joueur
        """       
        return self.sprites.field[img_id].get_image(1)
            
class Sprite:
    """
    il n'y a rien ici, mais si tu veux que ça marche laisse ça là
    """