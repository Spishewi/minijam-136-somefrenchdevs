import pygame, math


class LifeBar:
    def __init__(self, center_position: pygame.Vector2, width: int, height: int) -> None:
        self.height = max(height, 3)
        self.width = max(width, 3)
        self.position = center_position*16
        
    def draw(self, draw_surface: pygame.Surface, remplissage: float):
        bords = pygame.Rect(self.position.x - self.width / 2, self.position.y - self.height / 2, math.ceil(self.width), self.height)
        fond = pygame.Rect(self.position.x - self.width / 2 + 1, self.position.y - self.height / 2 + 1, math.ceil(self.width - 2), self.height - 2)
        vie = pygame.Rect(self.position.x - self.width / 2 + 1, self.position.y - self.height / 2 + 1, math.ceil(self.width - 2)*remplissage, self.height - 2)
        
        pygame.draw.rect(draw_surface, (200, 200, 200), bords, border_radius=2)
        pygame.draw.rect(draw_surface, (100, 100, 100), fond)
        pygame.draw.rect(draw_surface, (200, 0, 0), vie)
        
    def update(self, position: pygame.Vector2):
        self.position = position