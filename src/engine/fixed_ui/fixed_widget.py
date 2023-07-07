from __future__ import annotations
import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine.fixed_ui.widget_theme import Widget_theme

class Widget():
    def __init__(self, theme: Widget_theme) -> None:
        self._theme = theme
        self._width = 0
        self._height = 0

        self._first_draw = True

        self._last_surface_offset = pygame.Vector2()

    width = property(lambda self: self._width)
    height = property(lambda self: self._height)

    def draw(self, coordinates: pygame.Vector2, draw_surface: pygame.Surface) -> None:
        self._last_surface_offset = draw_surface.get_abs_offset()

    def update(self, dt: float) -> None:
        pass

    def event_handler(self, event: pygame.event.Event) -> None:
        pass

    