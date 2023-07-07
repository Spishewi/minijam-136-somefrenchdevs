from __future__ import annotations

import pygame

from engine.fixed_ui.fixed_widget import Widget
from engine.utils.hitbox import RectangularHitbox
from engine.utils.enumerations import Orientation

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from engine.fixed_ui.widget_theme import Widget_theme

from debug import debug

class Slider(Widget):
    def __init__(self, theme: Widget_theme, width: int, height: int, default_value: float = 0, orientation: Orientation = Orientation.HORIZONTAL) -> None:
        super().__init__(theme)

        self._width = width
        self._height = height

        self.value = default_value
        self.display_value = self.value
        self.orientation = orientation

        self.hovered = False
        self.grabbed = False

        self.last_coordinates = None

    def draw(self, coordinates: pygame.Vector2, draw_surface: pygame.Surface) -> None:
        super().draw(coordinates, draw_surface)

        if self._first_draw:
            mouse_pos = pygame.mouse.get_pos()
            hitbox = RectangularHitbox(coordinates, self.width, self.height)
            self.hovered = hitbox.collide_point(pygame.Vector2(mouse_pos) - self._last_surface_offset)
        
        if self.orientation == Orientation.HORIZONTAL:
            bar_rect = pygame.Rect(coordinates.x, round(coordinates.y+self.height/2-self._theme.slider_bar_width/2), self.width, self._theme.slider_bar_width)
            btn_rect = pygame.Rect(round(coordinates.x + (self.width - self._theme.slider_btn_width)*self.display_value), coordinates.y, self._theme.slider_btn_width, self.height)
            
        else:
            bar_rect = pygame.Rect(round(coordinates.x+self.width/2-self._theme.slider_bar_width/2), coordinates.y, self._theme.slider_bar_width, self.height)
            btn_rect = pygame.Rect(coordinates.x, round(coordinates.y + (self.height - self._theme.slider_btn_width)*self.display_value), self.width, self._theme.slider_btn_width)

        if self.hovered or self.grabbed:
            btn_background_color = self._theme.btn_hovered_background_color
            btn_outline_color = self._theme.btn_hovered_outline_color
        else:
            btn_background_color = self._theme.btn_background_color
            btn_outline_color = self._theme.btn_outline_color

        pygame.draw.rect(draw_surface, self._theme.slider_bar_color, bar_rect, border_radius=self._theme.slider_bar_width//2)
        pygame.draw.rect(draw_surface, btn_background_color, btn_rect, border_radius=self._theme.btn_border_radius)
        pygame.draw.rect(draw_surface, btn_outline_color, btn_rect, width=self._theme.btn_outline_width, border_radius=self._theme.btn_border_radius)

        self.last_coordinates = coordinates
        if self._first_draw:
            self._first_draw = False


    def event_handler(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEMOTION:
            if self.last_coordinates == None:
                return
            hitbox = RectangularHitbox(self.last_coordinates, self.width, self.height)
            self.hovered = hitbox.collide_point(pygame.Vector2(event.pos) - self._last_surface_offset)
            
        if event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            if event.button == pygame.BUTTON_LEFT:
                self.grabbed = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                self.grabbed = False


    def update(self, dt: float) -> None:
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - self._last_surface_offset
        
        if self.grabbed:
            if self.orientation == Orientation.HORIZONTAL:
                self.value = (mouse_pos.x - self.last_coordinates.x) / (self.width)
            else:
                self.value = (mouse_pos.y - self.last_coordinates.y) / (self.height)

        if self.value < 0:
            self.value = 0
        elif self.value > 1:
            self.value = 1
            
        if abs(self.display_value - self.value) < 0.001:
            self.display_value = self.value
        elif self.display_value != self.value:
            self.display_value += (self.value - self.display_value)*min(dt*10, 1)

    