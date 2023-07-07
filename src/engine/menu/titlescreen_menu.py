import pygame
from typing import TYPE_CHECKING
import os.path

from engine.fixed_ui.widget_theme import Widget_theme

from engine.fixed_ui.frame import Frame
from engine.fixed_ui.widgets.label import Label
from engine.fixed_ui.widgets.button import Button
from engine.fixed_ui.widgets.slider import Slider
from engine.fixed_ui.widgets.checkbox import Checkbox

from engine.utils.enumerations import AnchorX, AnchorY

from engine.scene.scene_event import SCENE_QUIT, SCENE_GAME_LAUNCH, SCENE_NEW_GAME_LAUNCH

from engine.utils.settings import debug_settings

class TitlescreenMenu():
    def __init__(self) -> None:
        self.theme = Widget_theme()
        self.theme.update(
            font_path = "../assets/font/PublicPixel.ttf",
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

        self.master = Frame()
        self._main()

        self.previous_menu = None

    def _main(self) -> None:
        self.previous_menu = None

        self.master.clear()
        self.master.grid_configure(7, 7)

        menu_title = Label(self.theme, "Menu principal", 20)
        
        if not os.path.exists("../saves/save.data"):
            disabled_theme = self.theme.deepcopy()
            disabled_theme.update(
                text_color = pygame.Color(127, 127, 127),
                hovered_text_color = pygame.Color(127, 127, 127),

                btn_background_color = pygame.Color(150, 150, 150),
                btn_hovered_background_color = pygame.Color(150, 150, 150),
                btn_outline_color = pygame.Color(127, 127, 127),
                btn_hovered_outline_color = pygame.Color(127, 127, 127),
            )
            play_btn = Button(disabled_theme, "Continuer", 15, lambda: None, height=50, width=250)
        else:
            play_btn = Button(self.theme, "Continuer", 15, lambda: pygame.event.post(pygame.event.Event(SCENE_GAME_LAUNCH)), height=50, width=250)
        new_game_btn = Button(self.theme, "Nouvelle partie", 15, lambda: pygame.event.post(pygame.event.Event(SCENE_NEW_GAME_LAUNCH)), height=50, width=250)
        settings_btn = Button(self.theme, "Options", 10, self._settings, height=40, width=100)
        quit_game_btn = Button(self.theme, "Quitter", 10, lambda: pygame.event.post(pygame.event.Event(SCENE_QUIT)), height=40, width=100)
        
        
        self.master.grid(menu_title, 1, 0, (AnchorX.CENTER, AnchorY.CENTER), column_span=7)

        
        self.master.grid(play_btn, 3, 0, (AnchorX.CENTER, AnchorY.CENTER), column_span=7)
        self.master.grid(new_game_btn, 4, 0, (AnchorX.CENTER, AnchorY.CENTER), column_span=7)
        self.master.grid(settings_btn, 5, 2, (AnchorX.CENTER, AnchorY.CENTER), column_span=2)
        self.master.grid(quit_game_btn, 5, 3, (AnchorX.CENTER, AnchorY.CENTER), column_span=2)

        return None

    def _settings(self) -> None:
        self.previous_menu = self._main

        self.master.clear()
        self.master.grid_configure(6, 1)

        menu_title = Label(self.theme, "OPTIONS", 20)

        graphics_settings = Button(self.theme, "Options graphiques", 15, self._graphics_settings, height=30)
        sound_settings = Button(self.theme, "Musiques et Sons", 15, self._sound_settings, height=30)
        keybinds_settings = Button(self.theme, "Contrôles", 15, self._keybinds_settings, height=30)
        debug_settings_btn = Button(self.theme, "Debug", 15, self._debug_settings, height=30)

        self.master.list(menu_title, margin_y=50, anchor_x=AnchorX.CENTER)

        self.master.list(graphics_settings, 10, 20, AnchorX.CENTER)
        self.master.list(sound_settings, 10, 20, AnchorX.CENTER)
        self.master.list(keybinds_settings, 10, 20, AnchorX.CENTER)

        
        if debug_settings.authorized:
            self.master.list(debug_settings_btn, 10, 20, AnchorX.CENTER)

    def _graphics_settings(self) -> None:
        self.previous_menu = self._settings

        self.master.clear()
        self.master.grid_configure(6, 1)

        menu_title = Label(self.theme, "OPTIONS GRAPHIQUES", 20)

        coming_soon = Label(self.theme, "COMING SOON", 15)

        self.master.list(menu_title, margin_y=50, anchor_x=AnchorX.CENTER)
        self.master.grid(coming_soon, 3, 0, (AnchorX.CENTER, AnchorY.CENTER))

    def _sound_settings(self) -> None:
        self.previous_menu = self._settings

        self.master.clear()
        self.master.grid_configure(6, 1)

        menu_title = Label(self.theme, "MUSIQUES ET SONS", 20)

        coming_soon = Label(self.theme, "COMING SOON", 15)

        self.master.list(menu_title, margin_y=50, anchor_x=AnchorX.CENTER)
        self.master.grid(coming_soon, 3, 0, (AnchorX.CENTER, AnchorY.CENTER))

    def _keybinds_settings(self) -> None:
        self.previous_menu = self._settings

        self.master.clear()
        self.master.grid_configure(6, 1)

        menu_title = Label(self.theme, "CONTRÔLES", 20)

        coming_soon = Label(self.theme, "COMING SOON", 15)

        self.master.list(menu_title, margin_y=50, anchor_x=AnchorX.CENTER)
        self.master.grid(coming_soon, 3, 0, (AnchorX.CENTER, AnchorY.CENTER))

    def _debug_settings(self) -> None:
        self.previous_menu = self._settings

        self.master.clear()
        self.master.grid_configure(6, 1)

        menu_title = Label(self.theme, "DEBUG", 20)

        menu_frame = Frame(scrollable=True)

        margin_x = 20
        alinea_x = 60
        margin_y = 10

        title_size = 15
        std_txt_size = 10

        checkbox_width = 15
        checkbox_height = 15

        sections_names = ["players", "bats", "fireflies", "tp_out", "spikes"]

        for section_name in sections_names:
            
            section_attribute = getattr(debug_settings, section_name)
            section_label = Label(self.theme, section_name.capitalize(), title_size)
            menu_frame.list(section_label, margin_x=margin_x, margin_y=margin_y)
            
            for item_name, item_value in section_attribute.to_dict().items():

                def f(state, section_attribute, item_name):
                    setattr(section_attribute, item_name, state)
                    debug_settings.save()

                item_label = Label(self.theme, item_name.capitalize(), std_txt_size)
                menu_frame.list(item_label, margin_x=alinea_x, margin_y=margin_y)

                item_checkbox = Checkbox(self.theme, checkbox_width, checkbox_height, item_value, None)
                item_checkbox.set_callback(f, section_attribute=section_attribute, item_name=item_name)
                menu_frame.list(item_checkbox, margin_x=alinea_x*2, margin_y=margin_y)

        self.master.list(menu_title, margin_y=50, anchor_x=AnchorX.CENTER)
        self.master.grid(menu_frame, 2, 0, row_span=4)
    

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