from __future__ import annotations
# std import
import pygame
import math

#nos import
from engine.utils.utilities import clamp
from engine.utils.settings import dev_settings

class Hitbox:
    def __init__(self, position: pygame.Vector2) -> None:
        self.pos = position

    def collide(self, hitbox: RectangularHitbox | CircularHitbox) -> bool:
        pass
    
    def collide_point(self, point: pygame.Vector2) -> bool:
        pass

    def __str__(self):
        return f"<{self.__class__.__name__} {self.pos}>"

    def __repr__(self):
        return str(self)
    
class RectangularHitbox(Hitbox):
    """
    Hitbox de forme rectangulaire
    """
    def __init__(self, position: pygame.Vector2, width: float, height: float) -> None:
        Hitbox.__init__(self, position)
        self.width = width
        self.height = height
        
    @property
    def bottom(self) -> float:
        return self.pos.y + self.height
    @bottom.setter
    def bottom(self, value:float):
        self.pos.y = value - self.height

    @property
    def right(self) -> float:
        return self.pos.x + self.width
    @right.setter
    def right(self, value:float):
        self.pos.x = value - self.width
        
    @property
    def center(self) -> pygame.Vector2:
        return pygame.Vector2(self.pos.x + self.width/2, self.pos.y + self.height/2)
    @center.setter
    def center(self, pos:pygame.Vector2):
        self.pos = pygame.Vector2(pos.x + self.width/2, pos.y + self.height/2)
        
    def collide(self, hitbox: RectangularHitbox | CircularHitbox) -> bool:
        
        if isinstance(hitbox, RectangularHitbox):
            if self.right <= hitbox.pos.x or hitbox.right <= self.pos.x :
                return False
            if self.bottom <= hitbox.pos.y  or hitbox.bottom <= self.pos.y :
                return False
            return True              
        
        if isinstance(hitbox, CircularHitbox):
            disc_to_rect = pygame.Vector2(clamp(hitbox.pos.x, self.pos.x, self.right), clamp(hitbox.pos.y, self.pos.y, self.bottom)) - hitbox.pos
            return True if disc_to_rect.magnitude_squared() < hitbox.radius**2 else False  
        
        raise TypeError(f"can not collide between RectangularHitbox and {type(hitbox)}")
        
    def collide_point(self, point: pygame.Vector2) -> bool:
        if self.pos.x + self.width <= point.x or point.x <= self.pos.x :
            return False
        if self.pos.y + self.height <= point.y  or point.y <= self.pos.y :
            return False
        return True

    def contains(self, hitbox: Hitbox) -> bool:
        if isinstance(hitbox, RectangularHitbox):
            if not (self.pos.x <= hitbox.pos.x and self.right >= hitbox.right):
                    return False
            if not (self.pos.y <= hitbox.pos.y and self.bottom >= hitbox.bottom):
                return False
            return True
        elif isinstance(hitbox, CircularHitbox):
            return self.contains(hitbox.get_rectangular_hitbox())
    
    def get_pygame_rect(self):
        """
        retourne un objet pygame.Rect. Attention, cette classe ne supporte que les nb entiers
        """
        return pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
    
    def get_drawable_rect(self, offset: pygame.Vector2, factor: float):
        rect = pygame.Rect((math.ceil(self.pos.x * factor * dev_settings.tile_size) + offset.x,
                             math.ceil(self.pos.y * factor * dev_settings.tile_size) + offset.y,
                             self.width * factor * dev_settings.tile_size,
                             self.height * factor * dev_settings.tile_size))
        return rect

    
    @staticmethod
    def from_pygame_rect(rect: pygame.Rect) -> Hitbox:
        return RectangularHitbox(pygame.Vector2(rect.x, rect.y), rect.width, rect.height)
    
    def copy(self):
        return RectangularHitbox(self.pos.copy(), self.width, self.height)


    def __str__(self):
        return f"<{self.__class__.__name__} ({self.pos}, {self.width}, {self.height})>"

    def __repr__(self):
        return str(self)
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, RectangularHitbox):
            return self.pos == __value.pos and self.height == __value.height and self.width == __value.width
        elif isinstance(__value, CircularHitbox):
            return False
        else:
            raise ValueError()
    
class CircularHitbox(Hitbox):
    def __init__(self, position: pygame.Vector2, radius: float) -> None:
        Hitbox.__init__(self, position)
        self.radius = radius

    @property
    def center(self) -> pygame.Vector2:
        return self.pos
    @center.setter
    def center(self, pos:pygame.Vector2):
        self.pos = pos
        
    def collide(self, hitbox: RectangularHitbox | CircularHitbox) -> bool:
        
        if isinstance(hitbox, CircularHitbox):
            distance_between_centers_squared = (self.pos.x-hitbox.pos.x)**2 + (self.pos.y - hitbox.pos.y)**2
            
            if distance_between_centers_squared < (self.radius + hitbox.radius)**2: #Circle intersects each other.
                return True
            return False
        
        if isinstance(hitbox, RectangularHitbox):
            DISC_to_rect = pygame.Vector2(clamp(self.pos.x, hitbox.pos.x, hitbox.right), clamp(self.pos.y, hitbox.pos.y, hitbox.bottom)) - self.pos
            return True if DISC_to_rect.magnitude_squared() < self.radius**2 else False  
    
    def collide_point(self, point: pygame.Vector2) -> bool:
        if (self.pos - point).magnitude_squared() > self.radius**2:
            return False
        return True
    
    def copy(self):
        return CircularHitbox(self.pos.copy(), self.radius)
    
    def get_rectangular_hitbox(self) -> RectangularHitbox:
        return RectangularHitbox(self.pos, self.radius*2, self.radius*2)
    
    
    def __str__(self):
        return f"<{self.__class__.__name__} ({self.pos}, {self.radius})>"

    def __repr__(self):
        return str(self)
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, RectangularHitbox):
            return False
        elif isinstance(__value, CircularHitbox):
            return self.pos == __value.pos and self.radius == __value.radius
        else:
            raise ValueError()