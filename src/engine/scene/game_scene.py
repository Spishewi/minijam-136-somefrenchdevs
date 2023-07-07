# std import
import pygame
import pickle
import os.path

# nos propre fichier import
from engine.utils.settings import dev_settings, debug_settings
#from engine.game.map.map_manager import MapManager, NEW_MAP_SET
from engine.camera.camera_view import CameraView
from engine.map.map_manager import MapManager
from engine.tower.tower_manager import TowerManager
from engine.wave.wave_manager import WaveManager
from engine.scene.scene import Scene
from engine.scene.scene_event import SCENE_TRANSITION_IN, SCENE_TRANSITION_OUT

from engine.menu.ingame_menu import IngameMenu

from engine.utils.enumerations import AnchorX, AnchorY, Orientation
from engine.utils.hitbox import RectangularHitbox

from engine.scene.scene_event import SCENE_QUIT

from debug import debug


class GameScene(Scene):
    """
    Le jeu en lui même
    """
    def __init__(self, scene_manager) -> None:
        super().__init__()
        self.scene_manager = scene_manager
        
    @Scene.load_decorator
    def load(self, new_game: bool):
        # Initializing the mapManager

        self.map_manager = MapManager("../assets/maps/maps.json")

        self.map_manager.load_map("map1") # not autoload in order to keep syncronous
        self.map_manager.set_map("map1")
        self.map_manager.current_map = self.map_manager.new_map_name
        
        pygame.event.post(pygame.Event(SCENE_TRANSITION_OUT))

        # Initializing the camera
        self.camera_view = CameraView(self.map_manager, move_ease=5)

        self.camera_view.set_zoom(1)

        # Initialiser les menus
        self.menu = IngameMenu()

        # vars
        self.new_map_set = False

        self.wave_manager = WaveManager(self.map_manager)
        self.tower_manager = TowerManager(self.map_manager)

        self.dt_multiplier = 1

    @Scene.update_decorator
    def update(self, dt: float):

        dt = dt * self.dt_multiplier
        # gestion des menus ------------------------------
        self.menu.update(dt)
        # gestion du jeu --------------------------------- 
        self.map_manager.update()
        self.wave_manager.update(dt)
        
        debug.add(self.map_manager._loading_maps)
        debug.add(self.map_manager._maps)
        debug.add(self.map_manager.current_map)

    @Scene.event_handler_decorator
    def event_handler(self, event: pygame.event.Event):
        self.menu.event_handler(event)
        self.tower_manager.event_handler(event)
        self.wave_manager.event_handler(event)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_F3:
                if debug_settings.authorized and event.mod & pygame.KMOD_ALT:
                    self.teleport_out("hub", "player_spawn_coords")
            
            if event.key == pygame.K_SPACE:
                self.dt_multiplier = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.dt_multiplier = 200
            
    @Scene.map_set_decorator
    def handle_map_set(self):
        if self.new_map_set:
            self.new_map_set = False
               
            self.map_manager.current_map = self.map_manager.new_map_name
            self.map_manager.clear_memory()
            
            self.camera_view.move(1, teleport=True)
    
    @Scene.draw_decorator
    def draw(self, draw_surface: pygame.Surface) -> None:
        self.camera_view.draw(draw_surface, self.tower_manager, self.wave_manager)
        
        self.menu.draw(draw_surface)


    def teleport_out(self, map_name: str, _destination_tp_name: str) -> None:
        self._destination_tp_name = _destination_tp_name
        pygame.event.post(pygame.Event(SCENE_TRANSITION_IN))
        self.scene_manager.is_transitioning_in = True

        self.map_manager.set_map(map_name, auto_load=True)