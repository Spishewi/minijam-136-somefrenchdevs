import pygame
import pytmx

from engine.map.map_manager import MapManager
from engine.wave.wave_manager import WaveManager 

from engine.scene.game_event import *
from engine.utils.sound import PLACE_TOWER_SOUND

from engine.tower.towers import MoneyTower, DamageTower

class TowerManager():
    def __init__(self, map_manager: MapManager, wave_manager: WaveManager) -> None:

        DamageTower.PRICE = 0
        MoneyTower.PRICE = 0

        self.map_manager = map_manager
        self.wave_manager = wave_manager

        self.grid_highlight_enabled = True
        self.towers: list[MoneyTower | DamageTower] = []

        self.selected_tower_type = None
        self.selected_tower = None

        self.authorized_placement_gid = self._get_placement_zone_gid(self.map_manager.get_current_map())

        self.money = 0
        self.total_money_earned = 0
        self.last_tower_click_tick = 0

        self._update_money()
        self._update_price()


    def update(self, dt: float) -> None:
        for tower in self.towers:
            tower.update(dt, self.wave_manager)
            
    def in_tower_zone(self):
        mousepos = self._get_relative_mouse_pos() // 16
        map = self.map_manager.get_current_map()
        zone_layer = map.get_layer_by_name("zone")

        for x in range(map.width):
            for y in range(map.height):
                if zone_layer.data[y][x] == self.authorized_placement_gid \
                    and mousepos.x == x and mousepos.y == y:
                        
                    return pygame.Vector2(x, y)

    def event_handler(self, event: pygame.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT:
            self.selected_tower_type = None
            self._update_price()
            self._highlight_tower(None)
            pygame.event.post(pygame.Event(UNSELECT_TOWER))
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            old_selected_tower = self.selected_tower
            
            pos = self.in_tower_zone()
            if pos:
                selected_tower = self._get_tower_at(pos)
    
                if selected_tower == None:
                    if self.selected_tower_type != None and self.selected_tower_type.PRICE <= self.money:
                        self.money -= self.selected_tower_type.PRICE
                        self.selected_tower_type.PRICE *= 1.7
                        if self.selected_tower_type.PRICE == 0:
                            if self.selected_tower_type == DamageTower:
                                self.selected_tower_type.PRICE = 80
                            else:
                                self.selected_tower_type.PRICE = 50
                        self.towers.append(self.selected_tower_type(pos))
                        PLACE_TOWER_SOUND.play()
                        self._update_money()
                else:
                    self.selected_tower_type = None
                    self._highlight_tower(selected_tower)
                    if old_selected_tower == selected_tower \
                        and isinstance(selected_tower, MoneyTower) \
                        and pygame.time.get_ticks()-self.last_tower_click_tick < 300:

                        selected_tower.harvest()
                    self.last_tower_click_tick = pygame.time.get_ticks()
                            
        
        elif event.type == SELECT_DAMAGE_TOWER:
            self.selected_tower_type = DamageTower
            self._update_price()
        elif event.type == SELECT_MONEY_TOWER:
            self.selected_tower_type = MoneyTower
            self._update_price()
        elif event.type == GIVE_MONEY:
            self.money += event.value
            if event.value > 0:
                self.total_money_earned += event.value
            self._update_money()
        elif event.type == UPGRADE_TOWER_RANGE:
            if self.money >= event.tower.range_price:
                self.money -= event.tower.range_price
                event.tower.shoot_range += 0.25
                event.tower.range_price **= 1.2
                self._update_money()
                self._menu_refresh()
        elif event.type == UPGRADE_TOWER_ATK:
            if self.money >= event.tower.atk_price:
                self.money -= event.tower.atk_price
                event.tower.atk *= 1.7
                event.tower.atk_price *= 2.1
                self._update_money()
                self._menu_refresh()
        elif event.type == UPGRADE_TOWER_SPEED:
            if self.money >= event.tower.speed_price:
                self.money -= event.tower.speed_price
                event.tower.shoot_speed *= 2.5/3
                event.tower.speed_price **= 1.2
                self._update_money()
                self._menu_refresh()
        elif event.type == UPGRADE_FIELD_SPEED:
            if self.money >= event.tower.speed_price:
                self.money -= event.tower.speed_price
                event.tower.upgrade_speed *= 2.5/3
                event.tower.speed_price *= 4
                self._update_money()
                self._menu_refresh()
        elif event.type == UPGRADE_FIELD_AMOUNT:
            if self.money >= event.tower.amount_price:
                self.money -= event.tower.amount_price
                event.tower.amount *= 1.75
                event.tower.amount_price **= 1.1
                self._update_money()
                self._menu_refresh()
        elif event.type == ENABLE_AUTO_HARVEST:
            if self.money >= event.tower.auto_harvest_price and event.tower.auto_harvest == False:
                self.money -= event.tower.auto_harvest_price
                event.tower.enable_auto_harvest()
                self._update_money()
                self._menu_refresh()
            
        
        for tower in self.towers:
            tower.event_handler(event)

    def draw(self, draw_surface: pygame.Surface) -> None:
        mousepos = self._get_relative_mouse_pos() // 16
        if 0 <= mousepos.x <= 15 and 0 <= mousepos.y <= 15 and self.selected_tower == None:
            self._draw_grid(draw_surface)

        towers = []
        for tower in self.towers:
            towers.append(tower.get_surface())
        towers.sort(key=lambda x: x[0].y)
        towers = [tower[1] for tower in towers]
        draw_surface.fblits(towers)

        for tower in self.towers:
            if isinstance(tower, DamageTower) and tower.target != None:
                pygame.draw.line(draw_surface, (255, 255, 255), tower.get_center()*16 + pygame.Vector2(0, -16), tower.target.get_center())

    def draw_ui(self, draw_surface: pygame.Surface) -> None:
        for tower in self.towers:
            tower.draw_ui(draw_surface)

        if self.selected_tower != None:
            pygame.draw.rect(draw_surface, (0, 255, 0), (self.selected_tower.position.x*16, self.selected_tower.position.y*16, 16, 16), width=1)
            if isinstance(self.selected_tower, DamageTower):
                pygame.draw.circle(draw_surface, (200, 255, 200), self.selected_tower.get_center()*16, self.selected_tower.shoot_range*16, 1)

        mousepos = self._get_relative_mouse_pos() / 16
        if self.selected_tower_type != None and 0 <= mousepos.x <= 16 and 0 <= mousepos.y <= 16:
            image = list(self.selected_tower_type.static_get_surface(mousepos))
            image[0] = image[0].copy()
            image[0].set_alpha(127)
            image[1] = (image[1][0]-8, image[1][1]-8)
            draw_surface.fblits([tuple(image)])

    def _get_relative_mouse_pos(self):
        map = self.map_manager.get_current_map()
        center_pos = pygame.Vector2(map.width, map.height) // 2
        const_hardcore = pygame.Vector2(pygame.display.get_surface().get_size()) / 2 - center_pos * 16
        mousepos = pygame.Vector2(pygame.mouse.get_pos()) - const_hardcore


        return mousepos
    
    def _get_tower_at(self, position: pygame.Vector2) -> bool:
        for tower in self.towers:
            if tower.position.x == position.x and tower.position.y == position.y:
                return tower
        return None

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
            
    def _highlight_tower(self, tower: DamageTower | MoneyTower | None):
        self.selected_tower = tower
        pygame.event.post(pygame.Event(SELECT_TOWER, {"tower": tower}))
            
    def _update_money(self):
        pygame.event.post(pygame.Event(MONEY_UPDATE, {"value": self.money}))
        
    def _menu_refresh(self):
        pygame.event.post(pygame.Event(REFRESH_MENU))

    def _update_price(self):
        if self.selected_tower_type == None:
            pygame.event.post(pygame.Event(PRICE_UPDATE, {"value": 0}))
        else:
            pygame.event.post(pygame.Event(PRICE_UPDATE, {"value": self.selected_tower_type.PRICE}))