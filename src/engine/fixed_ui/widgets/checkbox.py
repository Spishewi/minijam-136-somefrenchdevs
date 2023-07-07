from __future__ import annotations

import pygame

from engine.fixed_ui.fixed_widget import Widget
from engine.utils.hitbox import RectangularHitbox

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from engine.fixed_ui.widget_theme import Widget_theme

from debug import debug

class Checkbox(Widget):
    def __init__(self, theme: Widget_theme, width: int, height: int, default_state: bool = False, callback: function = None) -> None:
        super().__init__(theme)

        self.state = default_state
        self.callback = callback

        self.last_coordinates = None

        self.hovered = False

        self._width = width
        self._height = height


    def set_callback(self, callback, **params) -> None:
        self.callback = lambda x: callback(x, **params)

    def event_handler(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEMOTION:
            if self.last_coordinates == None:
                return
            hitbox = RectangularHitbox(self.last_coordinates, self.width, self.height)
            self.hovered = hitbox.collide_point(pygame.Vector2(event.pos) - self._last_surface_offset)
            
        if event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            if event.button == pygame.BUTTON_LEFT:
                self.state = not self.state
                if self.callback != None:
                    self.callback(self.state)

    def draw(self, coordinates: pygame.Vector2, draw_surface: pygame.Surface) -> None:
        super().draw(coordinates, draw_surface)

        if self._first_draw:
            mouse_pos = pygame.mouse.get_pos()
            hitbox = RectangularHitbox(coordinates, self.width, self.height)
            self.hovered = hitbox.collide_point(pygame.Vector2(mouse_pos) - self._last_surface_offset)
        
        background_rect = pygame.Rect(coordinates.x, coordinates.y, self.width, self.height)

        if self.hovered:
            background_color = self._theme.btn_hovered_background_color
            outline_color = self._theme.btn_hovered_outline_color
            check_color = self._theme.check_color
        else:
            background_color = self._theme.btn_background_color
            outline_color = self._theme.btn_outline_color
            check_color = self._theme.check_color

        pygame.draw.rect(draw_surface, background_color, background_rect, border_radius=self._theme.btn_border_radius)
        if self._theme.btn_outline_color != None:
            pygame.draw.rect(draw_surface, outline_color, background_rect, width=self._theme.btn_outline_width, border_radius=self._theme.btn_border_radius)

        if self.state:
            points = [(coordinates.x, coordinates.y + self.height/2), (coordinates.x + self.width/3, coordinates.y + 3 * self.height/4), (coordinates.x + self.width, coordinates.y)]
            pygame.draw.lines(draw_surface, check_color, False, points, self._theme.check_width)

        
        self.last_coordinates = coordinates
        if self._first_draw:
            self._first_draw = False