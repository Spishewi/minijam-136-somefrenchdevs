import pygame
from typing import TYPE_CHECKING
import os.path

from engine.fixed_ui.widget_theme import Widget_theme

from engine.fixed_ui.frame import Frame
from engine.fixed_ui.widgets.label import Label
from engine.fixed_ui.widgets.button import Button
from engine.fixed_ui.widgets.slider import Slider
from engine.fixed_ui.widgets.checkbox import Checkbox
from engine.utils.sound import set_sound_volume

from engine.utils.enumerations import AnchorX, AnchorY

from engine.scene.scene_event import SCENE_QUIT, SCENE_GAME_LAUNCH, SCENE_NEW_GAME_LAUNCH

from engine.utils.settings import debug_settings, user_settings

class TitlescreenMenu():
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
            btn_border_radius = 3,
            btn_outline_width = 2,
            btn_padding = 5,

            check_width = 3,
            check_color = pygame.Color(153, 255, 147),

            slider_bar_color = pygame.Color(50, 75, 100),
            slider_bar_width = 3
        )

        self.sfx_slider = None
        self.music_slider = None
        self.master = Frame()
        self._main()

        self.previous_menu = None

    def _main(self) -> None:
        self.previous_menu = None

        self.master.set_background(0)
        self.master.clear()
        self.master.grid_configure(7, 10)

        menu_title = Label(self.theme, "Another Tower Defense", 20)
        menu_title2 = Label(self.theme, "By Some French Devs", 8)
        
        new_game_btn = Button(self.theme, "New game", 15, lambda: pygame.event.post(pygame.event.Event(SCENE_NEW_GAME_LAUNCH)), height=50, width=250)
        settings_btn = Button(self.theme, "Settings", 10, self._settings, height=30, width=90)
        quit_game_btn = Button(self.theme, "Quit", 10, lambda: pygame.event.post(pygame.event.Event(SCENE_QUIT)), height=30, width=90)
        
        made_for_label = Label(self.theme, "Made for the Mini Jam 136: Cycles", 8)
        
        self.master.grid(menu_title, 1, 0, (AnchorX.CENTER, AnchorY.CENTER), column_span=10)
        self.master.grid(menu_title2, 2, 0, (AnchorX.CENTER, AnchorY.TOP), column_span=10)

        
        self.master.grid(new_game_btn, 3, 0, (AnchorX.CENTER, AnchorY.CENTER), column_span=10)
        self.master.grid(settings_btn, 5, 3, (AnchorX.CENTER, AnchorY.CENTER), column_span=2)
        self.master.grid(quit_game_btn, 5, 5, (AnchorX.CENTER, AnchorY.CENTER), column_span=2)

        self.master.grid(made_for_label, 6, 0, (AnchorX.CENTER, AnchorY.CENTER), column_span=10)
        
        return None

    def _settings(self) -> None:
        self.previous_menu = self._main

        self.master.set_background(0.5)

        self.master.clear()
        self.master.grid_configure(6, 1)

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
        self.master.draw(draw_surface)

    def event_handler(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.previous_menu != None:
                    self.master.clear()
                    self.previous_menu()

        self.master.event_handler(event)
    
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