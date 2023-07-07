import pygame
from typing import TYPE_CHECKING

from engine.fixed_ui.widget_theme import Widget_theme

from engine.fixed_ui.frame import Frame
from engine.fixed_ui.widgets.label import Label
from engine.fixed_ui.widgets.button import Button
from engine.fixed_ui.widgets.slider import Slider
from engine.fixed_ui.widgets.checkbox import Checkbox

from engine.utils.enumerations import AnchorX, AnchorY

from engine.scene.game_event import GAME_SAVE, GAME_SAVE_AND_QUIT

from engine.utils.settings import debug_settings


class IngameMenu():
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

        self.previous_menu = None
        self.opened = False

    def _main(self) -> None:
        self.previous_menu = None

        self.master.clear()
        self.master.grid_configure(6, 1)

        menu_title = Label(self.theme, "MENU", 20)

        settings_btn = Button(self.theme, "Options", 15, self._settings, height=30)
        save_btn = Button(self.theme, "Sauvegarder", 15, lambda: pygame.event.post(pygame.event.Event(GAME_SAVE)), height=30)
        quit_game_btn = Button(self.theme, "Quitter", 15, lambda: pygame.event.post(pygame.event.Event(GAME_SAVE_AND_QUIT)), height=30)
        
        
        self.master.list(menu_title, margin_y=50, anchor_x=AnchorX.CENTER)
        self.master.list(settings_btn, 10, 20, AnchorX.CENTER)
        self.master.list(save_btn, 10, 20, AnchorX.CENTER)
        self.master.list(quit_game_btn, 10, 20, AnchorX.CENTER)

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

        
        """
        players_label = Label(self.theme, "Players", title_size)
        menu_frame.list(players_label, margin_x=margin_x, margin_y=margin_y)

        
        players_rays_label = Label(self.theme, "rays", std_txt_size)
        menu_frame.list(players_rays_label, margin_x=margin_x, margin_y=margin_y)
        def f(state):
            debug_settings.players.rays = state
            debug_settings.save()
        players_rays_checkbox = Checkbox(self.theme, checkbox_width, checkbox_height, debug_settings.players.rays, f)
        menu_frame.list(players_rays_checkbox, margin_x=margin_x)

        bats_label = Label(self.theme, "Bats", title_size)
        menu_frame.list(bats_label, margin_x=margin_x, margin_y=margin_y)


        fireflies_label = Label(self.theme, "Fireflies", title_size)
        menu_frame.list(fireflies_label, margin_x=margin_x, margin_y=margin_y)"""

        self.master.list(menu_title, margin_y=50, anchor_x=AnchorX.CENTER)
        self.master.grid(menu_frame, 2, 0, row_span=4)
    

    def draw(self, draw_surface: pygame.Surface) -> None:
        self.master.draw(draw_surface)

    def event_handler(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.master.clear()
                if self.opened:
                    if self.previous_menu != None:
                        self.previous_menu()
                    else:
                        self.opened = False
                        self.master.set_background(0)

                else:
                    self._main()
                    self.opened = True
                    self.master.set_background(0.5)

        self.master.event_handler(event)
    
    def update(self, dt: float) -> None:
        self.master.update(dt)





"""
theme = Widget_theme()
theme.update(
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

self.test_label = Label(theme, "Hello World", 10)

#self.menu.grid(self.test_label, 1, 1, (AnchorX.LEFT, AnchorY.TOP))
#self.menu.grid(self.test_label, 0, 1, (AnchorX.LEFT, AnchorY.BOTTOM))



self.test_btn = Button(theme, "Hello World 2", 8, lambda: print("hello"))
self.menu.place(self.test_btn, pygame.Vector2(50, 50), (AnchorX.LEFT, AnchorY.TOP))

self.checkbox_test = Checkbox(theme, 25, 25)
self.menu.place(self.checkbox_test, pygame.Vector2(50, 100))

self.slider_test = Slider(theme, 200, 20, default_value=1, orientation=Orientation.HORIZONTAL)
self.menu.place(self.slider_test, pygame.Vector2(150, 150), anchor=(AnchorX.CENTER, AnchorY.CENTER))

self.secondary_frame = Frame(250, 200, scrollable=True)

for i in range(1):
    self.test_btn_2 = Button(theme, f"Hello World {i}", 8, lambda: print("hello 2"))
    self.secondary_frame.place(self.test_btn_2, pygame.Vector2(0, 20 * i), (AnchorX.LEFT, AnchorY.TOP))



self.menu.grid(self.secondary_frame, 1, 1)"""