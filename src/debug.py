# std import
import pygame

# nos fichier import
from engine.utils.settings import debug_settings

pygame.font.init() # needed
class Debug():
    font = pygame.font.Font("../assets/font/PublicPixel.ttf", debug_settings.font_size)

    def __init__(self, parent_surface: pygame.Surface = pygame.Surface((0,0)), enabled: bool = False) -> None:
        #setup debug
        pygame.init()
        self.font = Debug.font
        self.x = 10
        self.parent_surface = parent_surface
        self.reset()
        self.enabled = enabled
        self.tracked_dt = []
        self.tracked_dt_size = 200
        self.tracked_dt_display_scale = 7
        


    def add(self, *infos) -> None:
        if self.enabled:
            for info in infos:
                debug_surf = self.font.render(str(info), False, "White")
                debug_rect = debug_surf.get_rect(topleft = (self.x,self.y))
                pygame.draw.rect(self.debug_display_surface, (0, 0, 0, 100), debug_rect)
                self.debug_display_surface.blit(debug_surf, debug_rect)
                self.y += debug_settings.line_spacing

    def add_dt_track(self, dt: float) -> None:
        """
        to keep track of dt an better see lag spikes
        """
        if self.enabled:
            dt = dt * 1000 # seconds to milliseconds
            self.tracked_dt.append(dt)
            # suprime les dt les plus vieux pour garder les derniers
            if len(self.tracked_dt) > self.tracked_dt_size:
                self.tracked_dt.pop(1)

    def draw_dt_track(self):
        # on dessine les lignes à un pixel d'écart et calcule la couleur et la taille en fonction de dt 
        x = 0
        for dt in self.tracked_dt:
            pygame.draw.rect(self.debug_display_surface, (min(int(dt)*3, 255), max(75 - int(dt)*2, 0), 0, 255), pygame.Rect(x, self.debug_display_surface.get_rect().height - int(dt*self.tracked_dt_display_scale), 1, int(dt*self.tracked_dt_display_scale)))
            x += 1
    
    def display(self, surface: pygame.Surface) -> None:
        if self.enabled:
            self.draw_dt_track()
            self.parent_surface = surface
            self.parent_surface.blit(self.debug_display_surface, self.debug_display_surface.get_rect())
            self.reset()

    def reset(self) -> None:
        self.debug_display_surface = pygame.Surface((self.parent_surface.get_rect().width, self.parent_surface.get_rect().height), pygame.SRCALPHA)
        self.y = 10

    def enable(self) -> None:
        self.enabled = True
    
    def disable(self) -> None:
        self.enabled = False

    def toggle(self) -> bool:
        self.enabled = not self.enabled
        return self.enabled

    def get_state(self) -> bool:
        return self.enabled

debug = Debug()
debugfps = Debug()
debugfps.enable()