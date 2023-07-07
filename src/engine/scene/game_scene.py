# std import
import pygame
import pickle
import os.path

# nos propre fichier import
from engine.utils.settings import dev_settings, debug_settings
#from engine.game.map.map_manager import MapManager, NEW_MAP_SET
from engine.camera.camera_view import CameraView
from engine.map.map_manager import MapManager
from engine.scene.scene import Scene
from engine.scene.scene_event import SCENE_TRANSITION_IN, SCENE_TRANSITION_OUT

from engine.menu.ingame_menu import IngameMenu

from engine.utils.enumerations import AnchorX, AnchorY, Orientation
from engine.utils.hitbox import RectangularHitbox

from engine.scene.game_event import GAME_SAVE, GAME_SAVE_AND_QUIT
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

        
        # Loading save
        if os.path.exists("../saves/save.data") and not new_game:
            with open("../saves/save.data", "rb") as file:
                unpickler = pickle.Unpickler(file)
                save_dict = unpickler.load()
        else:
            save_dict = {
                "map_name": "level_0",
                "player_0_coords": None,
                "player_1_coords": None,
                "checkpoint": None
            }
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

    @Scene.update_decorator
    def update(self, dt: float):
        # gestion des menus ------------------------------
        self.menu.update(dt)
        # gestion du jeu --------------------------------- 
        self.map_manager.update()

        debug.add(self.map_manager._loading_maps)
        debug.add(self.map_manager._maps)
        debug.add(self.map_manager.current_map)

        object_manager = self.map_manager.get_current_objects_manager()
        object_manager.update(dt)

    @Scene.event_handler_decorator
    def event_handler(self, event: pygame.event.Event):
        self.menu.event_handler(event)
        object_manager = self.map_manager.get_current_objects_manager()
        object_manager.event_handler(event,
                                     tp_out_command = self.teleport_out)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_F3:
                if debug_settings.authorized and event.mod & pygame.KMOD_ALT:
                    self.teleport_out("hub", "player_spawn_coords")
        elif event.type == GAME_SAVE:
            self.save()
        elif event.type == GAME_SAVE_AND_QUIT:
            self.save()
            pygame.event.post(pygame.event.Event(SCENE_QUIT))
            
    @Scene.map_set_decorator
    def handle_map_set(self):
        if self.new_map_set:
            self.new_map_set = False
               
            self.map_manager.current_map = self.map_manager.new_map_name
            self.map_manager.clear_memory()
            
            self.camera_view.move(1, teleport=True)
    
    @Scene.draw_decorator
    def draw(self, draw_surface: pygame.Surface) -> None:
        self.camera_view.draw(draw_surface)
        self.menu.draw(draw_surface)


    def teleport_out(self, map_name: str, _destination_tp_name: str) -> None:
        self._destination_tp_name = _destination_tp_name
        pygame.event.post(pygame.Event(SCENE_TRANSITION_IN))
        self.scene_manager.is_transitioning_in = True

        self.map_manager.set_map(map_name, auto_load=True)

    def save(self):
        return
        save_dict = {"map_name": self.map_manager.current_map, "checkpoint": self._last_door_pos}
        for player in self.players:
            save_dict[f"player_{player.id}_coords"] = player.position
        
        with open("../saves/save.data", "wb") as file:
            pickler = pickle.Pickler(file, pickle.HIGHEST_PROTOCOL)
            pickler.dump(save_dict)