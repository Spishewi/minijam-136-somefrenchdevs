import pygame
from typing import TYPE_CHECKING
import copy

from engine.fixed_ui.widget_theme import Widget_theme

from engine.fixed_ui.frame import Frame
from engine.fixed_ui.widgets.label import Label
from engine.fixed_ui.widgets.button import Button
from engine.fixed_ui.widgets.slider import Slider
from engine.fixed_ui.widgets.checkbox import Checkbox

from engine.utils.enumerations import AnchorX, AnchorY

from engine.scene.game_event import *
from engine.scene.scene_event import *

from engine.tower.towers import DamageTower, MoneyTower
from engine.wave.wave_manager import WaveManager

from engine.utils.settings import debug_settings, user_settings
from engine.utils.sound import set_sound_volume
from engine.utils.utilities import number_to_str


class IngameMenu():
    def __init__(self) -> None:
        self.theme = Widget_theme()
        self.theme.update(
            font_path = "./assets/font/PublicPixel.ttf",
            text_color = pygame.Color(255, 255, 255),
            hovered_text_color = pygame.Color(150, 200, 250),

            btn_background_color = pygame.Color(200, 200, 200),
            btn_hovered_background_color = pygame.Color(75, 125, 175),
            btn_outline_color = pygame.Color(255, 255, 255),
            btn_hovered_outline_color = pygame.Color(125, 175, 225),
            btn_border_radius = 2,
            btn_outline_width = 1,
            btn_padding = 5,

            check_width = 3,
            check_color = pygame.Color(153, 255, 147),

            slider_bar_color = pygame.Color(50, 75, 100),
            slider_bar_width = 3

        )

        self.disabled_theme = copy.copy(self.theme)
        self.disabled_theme.update(
            text_color = pygame.Color(127, 127, 127),
            hovered_text_color = pygame.Color(127, 127, 127),

            btn_background_color = pygame.Color(150, 150, 150),
            btn_hovered_background_color = pygame.Color(150, 150, 150),
            btn_outline_color = pygame.Color(127, 127, 127),
            btn_hovered_outline_color = pygame.Color(127, 127, 127),
        )

        self.selected_tower_label = None
        
        self.selected_tower = "None"
        self.money_label = None
        self.money_value = 0
        self.price_value = 0

        self.sfx_slider = None
        self.music_slider = None
        
        self.need_refresh = False
        self.game_over = False
        self.game_info = {'wave': 0, 'kills': 0, 'money_earned': 0, 'village_health': 0, 'enemy_dmg': 0}

        self.paused = False

        self.master = Frame()
        self.current_menu_and_args = (None, None)
        
        
        self.money_label = Label(self.theme, f"Money: {number_to_str(self.money_value)}", 8)

        self.previous_menu = None
        self._select_tower_menu(None)

    def _select_tower_menu(self, tower) -> None:
        self.previous_menu = None
        self.current_menu_and_args = (self._select_tower_menu, tower)
        self.paused = False

        self.master.clear()
        self.master.set_background(0)
        self.master.grid_configure(6, 1)
        self._left_side()

        if isinstance(tower, MoneyTower):
            self._money_menu(tower)
        elif isinstance(tower, DamageTower):
            self._damage_menu(tower)
        else:
            self._default_menu()
        
        return None
    
    def _money_menu(self, tower: MoneyTower) -> None:
        menu_title = Label(self.theme, "FIELD", 8)

        if tower.status == 0:
            status = "seeded"
        elif tower.status == 1:
            status = "growing"
        else:
            status = "harvestable"
        growth_stage_label = Label(self.theme, "Growth stage:", 8)
        growth_stage_label2 = Label(self.theme, status, 8)

        if tower.status >= 2:
            harvest_btn = Button(self.theme, "Harvest", 8, tower.harvest, width=108)
        else:
            harvest_btn = Button(self.disabled_theme, "Harvest", 8, None, width=108)
            
        
        upgrade_label = Label(self.theme, "Upgrades", 8)
        
        if self.money_value >= tower.amount_price:
            upgrade_amount = Button(self.theme, f"Amount\n{number_to_str(tower.amount_price)}", 8, lambda: pygame.event.post(pygame.Event(UPGRADE_FIELD_AMOUNT, {'tower': tower})), width=108)
        else:
            upgrade_amount = Button(self.disabled_theme, f"Amount\n{number_to_str(tower.amount_price)}", 8, None, width=108)
            
        if self.money_value >= tower.speed_price:
            upgrade_speed = Button(self.theme, f"Speed\n{number_to_str(tower.speed_price)}", 8, lambda: pygame.event.post(pygame.Event(UPGRADE_FIELD_SPEED, {'tower': tower})), width=108)
        else:
            upgrade_speed = Button(self.disabled_theme, f"Speed\n{number_to_str(tower.speed_price)}", 8, None, width=108)
        
        if tower.auto_harvest:
            auto_harvest = Button(self.disabled_theme, f'Auto Harvest\nUnlocked', 8, None, width=108)
        elif self.money_value >= tower.auto_harvest_price:
            auto_harvest = Button(self.theme, f'Auto Harvest\n{number_to_str(tower.auto_harvest_price)}', 8, lambda: pygame.event.post(pygame.Event(ENABLE_AUTO_HARVEST, {'tower': tower})), width=108)
        else:
            auto_harvest = Button(self.disabled_theme, f'Auto Harvest\n{number_to_str(tower.auto_harvest_price)}', 8, None, width=108)
                   

        self.master.place(menu_title, pygame.Vector2(375, 20))
        self.master.place(self.money_label, pygame.Vector2(375, 40))
        self.master.place(growth_stage_label, pygame.Vector2(375, 60))
        self.master.place(growth_stage_label2, pygame.Vector2(380, 70))

        self.master.place(harvest_btn, pygame.Vector2(370, 100))
        
        self.master.place(upgrade_label, pygame.Vector2(375, 130))
        
        self.master.place(upgrade_amount, pygame.Vector2(370, 160))
        self.master.place(upgrade_speed, pygame.Vector2(370, 190))
        self.master.place(auto_harvest, pygame.Vector2(370, 220))
        

    def _damage_menu(self, tower: DamageTower) -> None:
        menu_title = Label(self.theme, "DAMAGE TOWER", 8)
        upgrade_label = Label(self.theme, "Upgrades", 8)
        
        if self.money_value >= tower.range_price:
            upgrade_range = Button(self.theme, f"Range\n{number_to_str(tower.range_price)}", 8, 
                                   lambda: pygame.event.post(pygame.Event(UPGRADE_TOWER_RANGE, {'tower': tower})), width=108)
        else:
            upgrade_range = Button(self.disabled_theme, f"Range\n{number_to_str(tower.range_price)}", 8, None, width=108)
        
        if self.money_value >= tower.atk_price:
            upgrade_atk = Button(self.theme, f"Damages\n{number_to_str(tower.atk_price)}", 8,
                                 lambda: pygame.event.post(pygame.Event(UPGRADE_TOWER_ATK, {'tower': tower})), width=108)
        else:
            upgrade_atk = Button(self.disabled_theme, f"Damages\n{number_to_str(tower.atk_price)}", 8, None, width=108)
        
        if self.money_value >= tower.speed_price:
            upgrade_speed = Button(self.theme, f"Speed\n{number_to_str(tower.speed_price)}", 8,
                                   lambda: pygame.event.post(pygame.Event(UPGRADE_TOWER_SPEED, {'tower': tower})), width=108)
        else:
            upgrade_speed = Button(self.disabled_theme, f"Speed\n{number_to_str(tower.speed_price)}", 8, None, width=108)
            
        
        self.master.place(menu_title, pygame.Vector2(375, 20))
        self.master.place(self.money_label, pygame.Vector2(375, 40))
        self.master.place(upgrade_label, pygame.Vector2(375, 60))
        
        self.master.place(upgrade_range, pygame.Vector2(370, 100))
        self.master.place(upgrade_atk, pygame.Vector2(370, 130))
        self.master.place(upgrade_speed, pygame.Vector2(370, 160))

    
    def _default_menu(self):
        menu_title = Label(self.theme, "SELECT TOWER", 8)

        selected_tower_title = Label(self.theme, "selected :", 8)
        self.selected_tower_label = Label(self.theme, self.selected_tower, 8)

        def select_damage_tower():
            pygame.event.post(pygame.Event(SELECT_DAMAGE_TOWER))
            self.selected_tower = "Damage tower"

        def select_money_tower():
            pygame.event.post(pygame.Event(SELECT_MONEY_TOWER))
            self.selected_tower = "Field"

        if self.money_value >= DamageTower.PRICE:
            damage_tower_btn = Button(self.theme, f"Damage tower\n{number_to_str(DamageTower.PRICE)}", 8, select_damage_tower, width=108)
        else:
            damage_tower_btn = Button(self.disabled_theme, f"Damage tower\n{number_to_str(DamageTower.PRICE)}", 8, None, width=108)
            
        if self.money_value >= MoneyTower.PRICE:
            money_tower_btn = Button(self.theme, f"Field\n{number_to_str(MoneyTower.PRICE)}", 8, select_money_tower, width=108)
        else:
            money_tower_btn = Button(self.disabled_theme, f"Field\n{number_to_str(MoneyTower.PRICE)}", 8, None, width=108)

        if self.money_value >= WaveManager.UPGRADE_VILLAGE_PRICE:
            village_upgrade = Button(self.theme, f"Village\nUpgrade\n{number_to_str(WaveManager.UPGRADE_VILLAGE_PRICE)}", 8, 
                                     lambda: pygame.event.post(pygame.Event(UPGRADE_VILLAGE)), width=108)
        else:
            village_upgrade = Button(self.disabled_theme, f"Village\nUpgrade\n{number_to_str(WaveManager.UPGRADE_VILLAGE_PRICE)}", 8, None, width=108)

        self.master.place(menu_title, pygame.Vector2(375, 20))

        self.master.place(self.money_label, pygame.Vector2(375, 40))

        self.master.place(selected_tower_title, pygame.Vector2(375, 60))
        self.master.place(self.selected_tower_label, pygame.Vector2(375, 70))

        self.master.place(damage_tower_btn, pygame.Vector2(370, 110))
        self.master.place(money_tower_btn, pygame.Vector2(370, 140))
        self.master.place(village_upgrade, pygame.Vector2(370, 170))
    
    def _game_over(self, waves: int, kills: int, total_money_earned: int):
        self.master.clear()
        self.master.set_background(0.5)
        self.game_over = True
        
        title = Label(self.theme, 'GAME OVER', 12)
        nb_waves = Label(self.theme, f'waves passed : {waves-1}', 8)
        nb_dead_enemies = Label(self.theme, f'killed enemies : {kills}', 8)
        money_earned = Label(self.theme, f'money earned : {number_to_str(total_money_earned)}', 8)
        
        button_title_screen = Button(self.theme, 'Titlescreen', 10, lambda: pygame.event.post(pygame.Event(SCENE_SET_TITLESCREEN)))
        
        
        self.master.place(title, pygame.Vector2(self.master.width/2, 80), (AnchorX.CENTER, AnchorY.CENTER))
        self.master.place(nb_waves, pygame.Vector2(self.master.width/2, 130), (AnchorX.CENTER, AnchorY.CENTER))
        self.master.place(nb_dead_enemies, pygame.Vector2(self.master.width/2, 150), (AnchorX.CENTER, AnchorY.CENTER))
        self.master.place(money_earned, pygame.Vector2(self.master.width/2, 170), (AnchorX.CENTER, AnchorY.CENTER))
        self.master.place(button_title_screen, pygame.Vector2(self.master.width/2, 200), (AnchorX.CENTER, AnchorY.CENTER))

    def _left_side(self):
        settings = Button(self.theme, 'Settings', 8, self._settings, width=108)
        
        nb_waves = Label(self.theme, f'Wave : {self.game_info["wave"]}', 8)
        nb_dead_enemies = Label(self.theme, f'Killed \nenemies : {self.game_info["kills"]}', 8)
        money_earned = Label(self.theme, f'Total money \nearned : {number_to_str(self.game_info["money_earned"])}', 8)

        village_health = Label(self.theme, f'Village life :\n{number_to_str(self.game_info["village_health"])}/{number_to_str(WaveManager.MAX_VILLAGE_LIFE)}', 8)

        enemy_dmg = Label(self.theme, f"Average enemy\ndamage : {number_to_str(self.game_info['enemy_dmg'])}", 8)

        self.master.place(settings, pygame.Vector2(2, 20))
        self.master.place(nb_waves, pygame.Vector2(2, 80))
        self.master.place(nb_dead_enemies, pygame.Vector2(2, 105))
        self.master.place(money_earned, pygame.Vector2(2, 140))

        self.master.place(village_health, pygame.Vector2(2, 175))

        self.master.place(enemy_dmg, pygame.Vector2(2, 210))

    def _settings(self):
        self.previous_menu = self._select_tower_menu(None)
        self.master.clear()
        self.master.set_background(0.5)
        self.master.grid_configure(6, 1)

        self.paused = True

        menu_title = Label(self.theme, "SETTINGS", 20)

        music_label = Label(self.theme, "Music volume", 8)
        self.music_slider = Slider(self.theme, 150, 15, user_settings.music)

        sfx_label = Label(self.theme, "Sound volume", 8)
        self.sfx_slider = Slider(self.theme, 150, 15, user_settings.sfx)

        self.master.list(menu_title, margin_y=35, anchor_x=AnchorX.CENTER)
        self.master.list(music_label, anchor_x=AnchorX.CENTER)
        self.master.list(self.music_slider, margin_y=15, anchor_x=AnchorX.CENTER)
        self.master.list(sfx_label, anchor_x=AnchorX.CENTER)
        self.master.list(self.sfx_slider, margin_y=15, anchor_x=AnchorX.CENTER)

    def draw(self, draw_surface: pygame.Surface) -> None:
        if self.need_refresh and not self.game_over and not self.paused:
            self.current_menu_and_args[0](self.current_menu_and_args[1])
            self.need_refresh = False
        self.master.draw(draw_surface)
        

    def event_handler(self, event: pygame.event.Event) -> None:
        self.master.event_handler(event)
        if event.type == MONEY_UPDATE:
            self.money_value = event.value
            if self.money_label != None:
                self.money_label.text = f"Money: {number_to_str(self.money_value)}"
            self.need_refresh = True
        if event.type == PRICE_UPDATE:
            self.price_value = event.value
            self.need_refresh = True
        if event.type == UNSELECT_TOWER:
            self.selected_tower = "None"
            self.need_refresh = True

        if event.type == SELECT_TOWER:
            self._select_tower_menu(event.tower)
        if event.type == REFRESH_MENU:
            self.need_refresh = True
    
    def update(self, dt: float) -> None:
        self.master.update(dt)
    

        if self.sfx_slider != None and self.sfx_slider.value != user_settings.sfx:
            user_settings.sfx = self.sfx_slider.value
            set_sound_volume(user_settings.sfx)
            user_settings.save()
        if self.music_slider != None and self.music_slider.value != user_settings.music:
            user_settings.music = self.music_slider.value
            pygame.mixer.music.set_volume(user_settings.music)
            user_settings.save()