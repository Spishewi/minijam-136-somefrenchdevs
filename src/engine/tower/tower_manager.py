import pygame
import pytmx
import math

from  engine.map.map_manager import MapManager

from engine.scene.game_event import *

from engine.tower.towers import MoneyTower, DamageTower

class TowerManager():
    def __init__(self, map_manager: MapManager) -> None:

        self.map_manager = map_manager

        self.grid_highlight_enabled = True
        self.towers: list[MoneyTower | DamageTower] = []

        self.selected_tower = MoneyTower

        self.authorized_placement_gid = self._get_placement_zone_gid(self.map_manager.get_current_map())

        self.money = 1000

        self._update_money()
        self._update_price()


    def update(self, dt: float) -> None:
        for tower in self.towers:
            tower.update(dt)

    def event_handler(self, event: pygame.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            mousepos = self._get_relative_mouse_pos() // 16
            map = self.map_manager.get_current_map()
            zone_layer = map.get_layer_by_name("zone")

            for x in range(map.width):
                for y in range(map.height):
                    pos = pygame.Vector2(x, y)
                    if zone_layer.data[y][x] == self.authorized_placement_gid \
                        and mousepos.x == x and mousepos.y == y:
                        if not self._is_tower_at(pos):
                            if self.selected_tower.DEFAULT_PRICE <= self.money:
                                self.money -= self.selected_tower.DEFAULT_PRICE
                                self.towers.append(self.selected_tower(pos))
                                self._update_money()
        
        elif event.type == SELECT_DAMAGE_TOWER:
            self.selected_tower = DamageTower
            self._update_price()
        elif event.type == SELECT_MONEY_TOWER:
            self.selected_tower = MoneyTower
            self._update_price()

        
        for tower in self.towers:
            tower.event_handler(event)

    def draw(self, draw_surface: pygame.Surface) -> None:
        mousepos = self._get_relative_mouse_pos() // 16
        if 0 <= mousepos.x <= 15 and 0 <= mousepos.y <= 15:
            self._draw_grid(draw_surface)

        towers = []
        for tower in self.towers:
            towers.append(tower.get_surface())
        towers.sort(key=lambda x: x[0].y)
        towers = [tower[1] for tower in towers]
        draw_surface.fblits(towers)

    def draw_ui(self, draw_surface: pygame.Surface) -> None:
        for tower in self.towers:
            tower.draw_ui(draw_surface)

    def _get_relative_mouse_pos(self):
        map = self.map_manager.get_current_map()
        center_pos = pygame.Vector2(map.width, map.height) // 2
        const_hardcore = pygame.Vector2(pygame.display.get_surface().get_size()) / 2 - center_pos * 16
        mousepos = pygame.Vector2(pygame.mouse.get_pos()) - const_hardcore


        return mousepos
    
    def _is_tower_at(self, position: pygame.Vector2) -> bool:
        for tower in self.towers:
            if tower.position.x == position.x and tower.position.y == position.y:
                return True
        return False

    def _draw_grid(self, draw_surface: pygame.Surface) -> None:

        # mousepos relative to tileset
        mousepos = self._get_relative_mouse_pos() // 16

        map = self.map_manager.get_current_map()
        zone_layer = map.get_layer_by_name("zone")

        hightlight_surface = pygame.Surface((16, 16))
        hightlight_surface.fill((255, 255, 255))
        hightlight_surface.set_alpha(40)
        
        for x in range(map.width):
            for y in range(map.height):
                if zone_layer.data[y][x] == self.authorized_placement_gid:
                    if(mousepos.x == x and mousepos.y == y):
                        hightlight_surface.set_alpha(75)    
                    else:
                        hightlight_surface.set_alpha(35)
                    draw_surface.blit(hightlight_surface, (x*16, y*16))

    def _get_placement_zone_gid(self, map: pytmx.TiledMap) -> int:
        for gid, properties in map.tile_properties.items():
            if "authorized_placement_zone" in properties:
                return gid
            
    def _update_money(self):
        pygame.event.post(pygame.Event(MONEY_UPDATE, {"value": self.money}))

    def _update_price(self):
        pygame.event.post(pygame.Event(PRICE_UPDATE, {"value": self.selected_tower.DEFAULT_PRICE}))