# std import
import pygame
import math

# nos propre fichier import
from engine.utils.settings import user_settings
from engine.utils.sound import *
from engine.scene.scene_event import *

# scenes
from engine.scene.game_scene import GameScene
from engine.map.map_manager import NEW_MAP_SET
from engine.scene.titlescreen_scene import TitlescreenScene

from debug import debug

class SceneManager():
    def __init__(self) -> None:
        # initialisation des modules
        pygame.init()
        
        flags = pygame.SCALED | pygame.RESIZABLE
        if user_settings.fullscreen:
            flags |= pygame.FULLSCREEN

        # initialisation de la fenêtre
        self.screen = pygame.display.set_mode((user_settings.window_width, user_settings.window_height), flags)
        icon = pygame.image.load("./assets/icon.png").convert_alpha()
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Another Tower Defense")


        #clock
        self.clock = pygame.time.Clock()
        #booléans
        self.is_loading = False
        self.is_transitioning_in = False
        
        self.need_transition_in = False
        self.need_transition_out = False
        self.start_transition_in = -1000
        self.start_transition_out = -1000

        #self.scene = GameScene()
        self.scene = TitlescreenScene()
        self.scene.load()

        pygame.mixer.music.load("./assets/sounds/triangular ideology-the fan sequel.ogg")
        pygame.mixer.music.set_volume(user_settings.music)
        pygame.mixer.music.play(loops=-1)

        set_sound_volume(user_settings.sfx)

    def event_handler(self, event):
        """
        Scene manager's event handler.
        """
        if event.type == SCENE_QUIT:
            self.handle_quit()
        elif event.type == SCENE_SET:
            ...
        elif event.type == SCENE_SET_LOADINGSCREEN:
            self.is_loading = True
        elif event.type == SCENE_REMOVE_LOADINGSCREEN:
            self.is_loading = False
            if isinstance(self.scene, GameScene):
                self.need_transition_out = True
        elif event.type == SCENE_GAME_LAUNCH:
            self.scene = GameScene(self)
            self.scene.load(new_game=False)
        elif event.type == SCENE_NEW_GAME_LAUNCH:
            self.scene = GameScene(self)
            self.scene.load(new_game=True)
        elif event.type == SCENE_SET_TITLESCREEN:
            self.scene = TitlescreenScene()
            self.scene.load()
        elif event.type == SCENE_TRANSITION_IN:
            self.need_transition_in = True
            self.is_transitioning_in = True
        elif event.type == SCENE_TRANSITION_OUT:
            self.need_transition_out = True
        elif event.type == pygame.KEYDOWN:
            # pour activer le debug
            if event.key == pygame.K_F3 and not (event.mod & pygame.KMOD_ALT):
                debug.toggle()
            # pour mettre en plein écran
            elif event.key == pygame.K_F11:
                # toggle le fullscreen
                pygame.display.toggle_fullscreen()
        elif event.type == NEW_MAP_SET:
            self.scene.new_map_set = True

        # pour faire crash quand il y a une erreur
        elif event.type == SCENE_LOADING_ERROR:
            raise event.error
        
        # quand la fenêtre est redimensionnée
        elif event.type == pygame.VIDEORESIZE:
            # le mettre au dimensions
            pygame.display._resize_event(event)
    
    def handle_quit(self):
        self.running = False

    def draw_loading_screen(self):        
        self.screen.fill((0, 0, 0)) # 64 127 127

        center_pos = pygame.Vector2(self.screen.get_size()) / 2
        ticks = pygame.time.get_ticks() / 1000
        size = 5
        nb = 15
        for i in range(nb):
            pos = center_pos.copy()
            pos.x += math.cos(ticks + i*2*math.pi/nb) * 30
            pos.y += math.sin(ticks + i*2*math.pi/nb) * 30
            pygame.draw.circle(self.screen, (255*(i/nb),)*3, pos, math.ceil(i/nb*size))
            
    def transitionning_in_or_not(self):
        time_now = pygame.time.get_ticks()
        
        return self.need_transition_in or time_now - self.start_transition_in <= 1000
            
    def toogle_transition(self):
        time_now = pygame.time.get_ticks()
        if self.need_transition_in :
            self.start_transition_in = time_now
            self.need_transition_in = False
        
        if time_now - self.start_transition_in <= 1050:
            self.draw_transition(time_now, self.start_transition_in)
        elif self.need_transition_out:
            self.start_transition_out = time_now
            self.need_transition_out = False
            
        if time_now - self.start_transition_out <= 1000:
            self.draw_transition(time_now, self.start_transition_out, reverse=True)
        
    def draw_transition(self, now: float, start: float, reverse: bool = False):
        draw_surface = pygame.Surface(self.screen.get_size())
        draw_surface.fill((255,255,255))
        
        if not reverse:
            circle_radius = max(min(1000 - (now - start), 1000), 0)
        else:
            circle_radius = max(min(now - start, 1000), 0)
        
        pygame.draw.circle(draw_surface, (0,0,0), (draw_surface.get_width()//2, draw_surface.get_height()//2), math.ceil(circle_radius/1000*draw_surface.get_width()))
        self.screen.blit(draw_surface, (0, 0), special_flags=pygame.BLEND_SUB)
        
        
        draw_surface.fill((83*0.8, 120*0.8, 111*0.8))

        if not reverse:
            circle_radius = max(min(1000 - (now - start), 1000), 0)
        else:
            circle_radius = max(min(now - start, 1000), 0)
        
        pygame.draw.circle(draw_surface, (0,0,0), (draw_surface.get_width()//2, draw_surface.get_height()//2), math.ceil(circle_radius/1000*draw_surface.get_width()))
        self.screen.blit(draw_surface, (0, 0), special_flags=pygame.BLEND_ADD)

    def run(self):
        self.running = True
        while self.running:
            # clear the screen
            self.screen.fill((0, 0, 0))
            
            # récupération de dt et limitation des fps ---------------
            dt = self.clock.tick(user_settings.fps) / 1000
            dt = min(dt, 0.5) # sécurité pour empécher les gros lag spikes

            self.is_transitioning_in = self.transitionning_in_or_not()
            
            # la boucle des events -----------------------------------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.handle_quit()
                self.event_handler(event)
                
                if not self.is_loading and not self.is_transitioning_in:
                    self.scene.event_handler(event)
                    
            if not (self.is_loading or self.is_transitioning_in) and isinstance(self.scene, GameScene):
                self.scene.handle_map_set()

            # debugs adds ------------------------------------------
            debug.add(f"FPS: {self.clock.get_fps():.2f}")
            debug.add("") # retour à la ligne

            #debug.add_dt_track(dt)
            self.scene.draw(self.screen)
                
            self.toogle_transition()

            if self.is_loading and not self.is_transitioning_in:
                self.draw_loading_screen()
            elif not self.is_transitioning_in :
                self.scene.update(dt)

            # draw debug
            debug.display(self.screen)

            pygame.display.update()