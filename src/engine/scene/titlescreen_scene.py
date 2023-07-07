# std import
import pygame

# nos propre fichier import
from engine.utils.settings import dev_settings, debug_settings

from engine.scene.scene import Scene
from engine.menu.titlescreen_menu import TitlescreenMenu


class TitlescreenScene(Scene):
    def __init__(self) -> None:
        super().__init__()
        
    @Scene.load_decorator
    def load(self):
        
        self.menu = TitlescreenMenu()
        
        #controller_manager.set_mouse_grab(True)

    @Scene.update_decorator
    def update(self, dt: float):
        # gestion des menus ------------------------------
        self.menu.update(dt)

    @Scene.event_handler_decorator
    def event_handler(self, event: pygame.event.Event):
        self.menu.event_handler(event)

    
    @Scene.draw_decorator
    def draw(self, draw_surface: pygame.Surface) -> None:
        self.menu.draw(draw_surface)