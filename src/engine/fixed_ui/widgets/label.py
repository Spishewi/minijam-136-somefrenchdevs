from __future__ import annotations

import pygame
from typing import TYPE_CHECKING
from engine.fixed_ui.fixed_widget import Widget

if TYPE_CHECKING:
    from engine.fixed_ui.widget_theme import Widget_theme

class Label(Widget):
    def __init__(self, theme: Widget_theme, text: str, font_size: int) -> None:
        super().__init__(theme)

        self.text = text
        self.font_size = font_size

        self.font = pygame.font.Font(self._theme.font_path, self.font_size)

        self._render()

    def _render(self):
        self._rendered_text_surface = self.font.render(self.text, False, self._theme.text_color)
        self._rendered_text = self.text

        self._width = self._rendered_text_surface.get_width()
        self._height = self._rendered_text_surface.get_height()

    def draw(self, coordinates: pygame.Vector2, draw_surface: pygame.Surface):
        super().draw(coordinates, draw_surface)
        
        if self._rendered_text_surface == None or self._rendered_text != self.text:
            self._render()
        
        draw_surface.blit(self._rendered_text_surface, coordinates)