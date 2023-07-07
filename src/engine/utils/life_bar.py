import pygame


class LifeBar:
    def __init__(self, center_position: pygame.Vector2, width: int, height: int, remplissage: float) -> None:
        self.height = max(height, 3)
        self.width = max(width, 3)
        self.position = center_position*16
        self.remplissage = remplissage
        
    def draw(self, draw_surface: pygame.Surface):
        bords = pygame.Rect(self.position.x - self.width / 2, self.position.y - self.height / 2, self.width, self.height)
        fond = pygame.Rect(self.position.x - self.width / 2 + 1, self.position.y - self.height / 2 + 1, self.width - 2, self.height - 2)
        vie = pygame.Rect(self.position.x - self.width / 2 + 1, self.position.y - self.height / 2 + 1, (self.width - 2)*self.remplissage, self.height - 2)
        
        pygame.draw.rect(draw_surface, (200, 200, 200), bords, border_radius=5)
        pygame.draw.rect(draw_surface, (200, 200, 200), fond, border_radius=5)
        pygame.draw.rect(draw_surface, (200, 200, 200), vie, border_radius=5)
        
    def update(self, remplissage: float):
        self.remplissage = remplissage