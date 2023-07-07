from __future__ import annotations
from typing import TYPE_CHECKING

import pygame
import json

from engine.utils.image import DynamicImage
from engine.utils.enumerations import Gravity
from engine.utils.settings import Settings

if TYPE_CHECKING:
    from objects.entities.player.player import Player
    from objects.entities.bats import Bat
    from objects.entities.firefly import Firefly
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
                rect = (v[0][0] * self.settings.sprite_width, v[0][1] * self.settings.sprite_width, self.settings.sprite_width, self.settings.sprite_width)
                tile_surface = pygame.Surface((self.settings.sprite_width, self.settings.sprite_width), pygame.SRCALPHA)
                tile_surface.blit(spritesheet, (0, 0), rect)
                setattr(sprites, k, DynamicImage(tile_surface))
            else:
                sprite_list = []
                for x in range(v[0][0], v[1][0]+1):
                    for y in range(v[0][1], v[1][1]+1):
                        rect = (x * self.settings.sprite_width, y * self.settings.sprite_width, self.settings.sprite_width, self.settings.sprite_width)
                        tile_surface = pygame.Surface((self.settings.sprite_width, self.settings.sprite_width), pygame.SRCALPHA)
                        tile_surface.blit(spritesheet, (0, 0), rect)
                        sprite_list.append(DynamicImage(tile_surface))
                setattr(sprites, k, sprite_list)

        return sprites
    


class PlayerAnimation(Animation):
    def __init__(self, path: str, player: Player) -> None:
        Animation.__init__(self, path)
        
        self.player = player   
        self.last_idle = pygame.time.get_ticks()
        self.reset_run_animation = True
        self.x_velocity = 1
        self.y_velocity = 1
        
    def get_curent_animation(self, factor:float) -> pygame.Surface:     
        """
        renvoie une surface pygame contenant l'image du joueur
        cette image est choisie en fonction des mouvements du joueur
        """       
        
        # grappiné
        if self.player.swing:
            self.last_idle = pygame.time.get_ticks()
            
            if not self.player.collide[self.player.gravity_orientation]:
                anchor = self.player.anchors[-1]
                rope_vector = pygame.Vector2(self.player.get_center().x - anchor.x,self.player.get_center().y - anchor.y)
                
                rope_velocity_determinant_is_strictly_positif = rope_vector.x * self.player.velocity.y - rope_vector.y * self.player.velocity.x > 0
                if rope_velocity_determinant_is_strictly_positif:
                    angle = (-pygame.math.Vector2(0, 1).angle_to(rope_vector))%90
                else:
                    angle = pygame.math.Vector2(0, 1).angle_to(rope_vector)%90

                if angle >= 67.5:
                    sprite = self.sprites.swing[0].get_image(factor)
                elif angle >= 45:
                    sprite = self.sprites.swing[1].get_image(factor)
                elif angle >= 22.5:
                    sprite = self.sprites.swing[2].get_image(factor)
                else:
                    sprite = self.sprites.swing[3].get_image(factor)

                if rope_velocity_determinant_is_strictly_positif:
                    sprite = pygame.transform.flip(sprite, True, False)
                    if rope_vector.x > 0 and rope_vector.y > 0:
                        sprite = pygame.transform.rotate(sprite, -270)
                    elif rope_vector.x > 0 and rope_vector.y < 0:
                        sprite = pygame.transform.rotate(sprite, -180)
                    elif rope_vector.x < 0 and rope_vector.y < 0:
                        sprite = pygame.transform.rotate(sprite, -90)
                else:
                    if rope_vector.x > 0 and rope_vector.y < 0:
                        sprite = pygame.transform.rotate(sprite, 90)
                    elif rope_vector.x < 0 and rope_vector.y < 0:
                        sprite = pygame.transform.rotate(sprite, 180)
                    elif rope_vector.x < 0 and rope_vector.y >0:
                        sprite = pygame.transform.rotate(sprite, 270)
                return sprite

        # On change les axes si la gravité n'est pas vers la bas
        if self.player.gravity_orientation == Gravity.LEFT:
            if self.player.velocity.y != 0:
                self.x_velocity = self.player.velocity.y
            if self.player.velocity.x != 0:
                self.y_velocity = -self.player.velocity.x
        elif self.player.gravity_orientation == Gravity.UP:
            if self.player.velocity.x != 0:
                self.x_velocity = -self.player.velocity.x
            if self.player.velocity.y != 0:
                self.y_velocity = -self.player.velocity.y
        elif self.player.gravity_orientation == Gravity.RIGHT:
            if self.player.velocity.y != 0:
                self.x_velocity = -self.player.velocity.y
            if self.player.velocity.x != 0:
                self.y_velocity = self.player.velocity.x
        else:
            if self.player.velocity.x != 0:
                self.x_velocity = self.player.velocity.x
            if self.player.velocity.y != 0:
                self.y_velocity = self.player.velocity.y
                
        # saut et chutes
        if self.player.air_time>0.2 or self.player.is_jumping:
            self.last_idle = pygame.time.get_ticks()
            if self.x_velocity < 0:
                sprite = pygame.transform.flip(self.sprites.jump.get_image(factor), True, False)
            else:
                sprite = self.sprites.jump.get_image(factor)
        
        # course
        elif self.player.velocity != pygame.Vector2(0, 0):
            self.last_idle = pygame.time.get_ticks()
            sprite_id = int((pygame.time.get_ticks())/90%10)
            if self.x_velocity < 0:
                sprite = pygame.transform.flip(self.sprites.run[sprite_id].get_image(factor), True, False)
            else:
                sprite = self.sprites.run[sprite_id].get_image(factor)
        
        # immobile
        elif pygame.time.get_ticks() - self.last_idle <= 10000:
            self.reset_seat = True
            if self.x_velocity < 0:
                sprite = pygame.transform.flip(self.sprites.idle[1].get_image(factor), True, False)
            else:
                sprite = self.sprites.idle[1].get_image(factor)
        # assis
        else:
            if self.reset_seat:
                self.reset_seat = False
                self.start_sitting_tick = pygame.time.get_ticks()
            # assis
            tick = pygame.time.get_ticks() - self.start_sitting_tick
            if tick <= 350:
                sprite = self.sprites.idle[0].get_image(factor)
            elif tick <= 700:
                sprite = self.sprites.seat[0].get_image(factor)
            elif tick <= 1050:
                sprite = self.sprites.seat[1].get_image(factor)
            else:
                sprite = self.sprites.seat[2].get_image(factor)
        
        if self.player.gravity_orientation == Gravity.DOWN:
            return sprite
        if self.player.gravity_orientation == Gravity.LEFT:
            return pygame.transform.rotate(sprite,-90)
        if self.player.gravity_orientation == Gravity.UP:
            return pygame.transform.rotate(sprite,-180)
        return pygame.transform.rotate(sprite,-270)

class Sprite:
    """
    il n'y a rien ici, mais si tu veux que ça marche laisse ça là
    """