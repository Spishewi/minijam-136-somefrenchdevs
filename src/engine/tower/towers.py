import pygame
import math

class Tower():
    DEFAULT_PRICE = 0
    def __init__(self, position) -> None:
        self.position = position.copy()

        self.color = (255, 255, 255)

    def update(self, dt: float) -> None:
        ...

    def event_handler(self, event: pygame.Event) -> None:
        ...

    def draw_ui(self,  draw_surface: pygame.Surface) -> None:
        ...


class DamageTower(Tower):
    DEFAULT_PRICE = 100
    CONVERTED = False
    IMAGE = pygame.image.load('../assets/towers/damage.png')
    def __init__(self, position) -> None:
        super().__init__(position)
        if not DamageTower.CONVERTED:
            DamageTower.CONVERTED = True
            DamageTower.IMAGE = DamageTower.IMAGE.convert_alpha()
        self.color = (255, 0, 0)
        
    def get_surface(self) -> tuple[pygame.Vector2, tuple[pygame.Surface, tuple[int, int]]]:
        return (self.position, (DamageTower.IMAGE, (self.position.x*16, self.position.y*16 - 16)))

class MoneyTower(Tower):
    DEFAULT_PRICE = 50
    CONVERTED = False
    IMAGE = pygame.image.load('../assets/towers/money.png')
    def __init__(self, position) -> None:
        super().__init__(position)
        if not MoneyTower.CONVERTED:
            MoneyTower.CONVERTED = True
            MoneyTower.IMAGE = MoneyTower.IMAGE.convert_alpha()

        self.color = (255, 255, 0)
        
    def get_surface(self) -> tuple[pygame.Vector2, tuple[pygame.Surface, tuple[int, int]]]:
        return (self.position, (MoneyTower.IMAGE, (self.position.x*16, self.position.y*16)))