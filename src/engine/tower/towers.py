import pygame
import math

from debug import debug

from engine.wave.wave_manager import WaveManager
from engine.utils.animations import FieldAnimation

from engine.scene.game_event import *

class Tower():
    PRICE = 0
    def __init__(self, position) -> None:
        self.position = position.copy()

        self.color = (255, 255, 255)

    def update(self, dt: float, wave_manager: WaveManager) -> None:
        ...

    def event_handler(self, event: pygame.Event) -> None:
        ...

    def draw_ui(self,  draw_surface: pygame.Surface) -> None:
        ...


class DamageTower(Tower):
    PRICE = 0
    CONVERTED = False
    IMAGE = pygame.image.load('./assets/towers/damage.png')
    def __init__(self, position) -> None:
        super().__init__(position)
        if not DamageTower.CONVERTED:
            DamageTower.CONVERTED = True
            DamageTower.IMAGE = DamageTower.IMAGE.convert_alpha()



        self.color = (255, 0, 0)
        self.shoot_range = 3
        self.shoot_speed = 1000
        self.target = None
        
        self.range_price = 60
        self.atk_price = 60
        self.speed_price = 60

        self.atk = 2

        self.custom_ticks = 0
        
    @staticmethod
    def static_get_surface(position: pygame.Vector2) -> tuple[pygame.Surface, tuple[int, int]]:
        return (DamageTower.IMAGE, (position.x*16, position.y*16 - 16))
    
    def get_surface(self) -> tuple[pygame.Vector2, tuple[pygame.Surface, tuple[int, int]]]:
        return (self.position, DamageTower.static_get_surface(self.position))
    
    def update(self, dt: float, wave_manager: WaveManager) -> None:
        self._update_target(wave_manager)

        if self.target != None:
            self.custom_ticks += dt * 1000
            while self.custom_ticks >= self.shoot_speed:
                self.custom_ticks -= self.shoot_speed
                self._shoot(wave_manager)
        else:
            self.custom_ticks = 0

    def get_center(self):
        return self.position + pygame.Vector2(0.5, 0.5)
    
    def _shoot(self, wave_manager: WaveManager):
        if self.target != None:
            self.target.health -= self.atk
            self._update_target(wave_manager)
        

    def _update_target(self, wave_manager: WaveManager):
        if self.target != None and self.target.health <= 0:
            self.target.must_be_deleted = True
            self.target = None
        self._select_target(wave_manager)

    def _select_target(self, wave_manager: WaveManager) -> None:
        if self.target == None or (self.target.get_center()/16 - self.get_center()).magnitude_squared() > self.shoot_range**2:
            for i in range(len(wave_manager.enemies)):
                enemy = wave_manager.enemies[i]
                if (enemy.get_center()/16 - self.get_center()).magnitude_squared() < self.shoot_range**2 and not enemy.must_be_deleted:
                    self.target = enemy
                    return
            self.target = None

class MoneyTower(Tower):
    PRICE = 0
    CONVERTED = False
    IMAGE = pygame.image.load('./assets/towers/money.png')
    def __init__(self, position) -> None:
        super().__init__(position)
        if not MoneyTower.CONVERTED:
            MoneyTower.CONVERTED = True
            MoneyTower.IMAGE = MoneyTower.IMAGE.convert_alpha()

        self.amount = 10
        self.upgrade_speed = 3000
        self.status = 0
        self.auto_harvest = False
        
        self.speed_price = 60
        self.amount_price = 60
        self.auto_harvest_price = 200
        
        self.custom_ticks = 0
        self.animation = FieldAnimation('./assets/towers/money_animation')

    @staticmethod
    def static_get_surface(position: pygame.Vector2) -> tuple[pygame.Surface, tuple[int, int]]:
        return (MoneyTower.IMAGE, (position.x*16, position.y*16))
        
    def get_surface(self) -> tuple[pygame.Vector2, tuple[pygame.Surface, tuple[int, int]]]:
        return (self.position, (self.animation.get_curent_animation(min(2, self.status)), (self.position.x*16, self.position.y*16)))
    
    def update(self, dt: float, *args) -> None:
        self.custom_ticks += dt * 1000
        while self.custom_ticks >= self.upgrade_speed:
            self.custom_ticks -= self.upgrade_speed
            self.status += 1
            pygame.event.post(pygame.Event(REFRESH_MENU))
            if self.auto_harvest and self.status >= 3:
                self.harvest()
                
    def harvest(self):
        if self.status >= 2:
            self.status = 0
            pygame.event.post(pygame.Event(GIVE_MONEY, {'value': self.amount}))
            pygame.event.post(pygame.Event(REFRESH_MENU))
            
            
    def enable_auto_harvest(self):
        self.auto_harvest = True