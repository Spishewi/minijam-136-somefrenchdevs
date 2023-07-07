from __future__ import annotations

import pygame

from engine.fixed_ui.fixed_widget import Widget
from engine.utils.hitbox import RectangularHitbox

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from engine.fixed_ui.widget_theme import Widget_theme

class Button(Widget):
    def __init__(self, theme: Widget_theme, text:str, font_size: int, callback: function = None, width: int = None, height: int = None) -> None:
        super().__init__(theme)

        self.text = text
        self.font_size = font_size
        self.callback = callback

        self.font = pygame.font.Font(self._theme.font_path, self.font_size)

        self.hovered = False

        self.last_coordinates = None
        

        self._fixed_width = width != None
        self._width = width

        self._fixed_height = height != None
        self._height = height

        self._render()

    def _render(self):
        self._rendered_text_surface = self.font.render(self.text, False, self._theme.text_color)
        
        if self._theme.hovered_text_color != None:
            self._rendered_hovered_text_surface = self.font.render(self.text, False, self._theme.hovered_text_color)
        else:
            self._rendered_hovered_text_surface = self._rendered_text_surface
        
        self._rendered_text = self.text

        if not self._fixed_width:
            self._width = self._rendered_text_surface.get_width() + self._theme.btn_padding * 2
        if not self._fixed_height:
            self._height = self._rendered_text_surface.get_height() + self._theme.btn_padding * 2

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
                if self.callback != None:
                    self.callback()
                

    def draw(self, coordinates: pygame.Vector2, draw_surface: pygame.Surface):
        super().draw(coordinates, draw_surface)

        if self._first_draw:
            mouse_pos = pygame.mouse.get_pos()
            hitbox = RectangularHitbox(coordinates, self.width, self.height)
            self.hovered = hitbox.collide_point(pygame.Vector2(mouse_pos) - self._last_surface_offset)

        if self._rendered_text_surface == None or self._rendered_hovered_text_surface == None or self._rendered_text != self.text:
            self._render()

        #debug.add(self.hovered)

        
        background_rect = pygame.Rect(coordinates.x, coordinates.y, self.width, self.height)
        if self.hovered:
            background_color = self._theme.btn_hovered_background_color
            outline_color = self._theme.btn_hovered_outline_color
            text_surface = self._rendered_hovered_text_surface
        else:
            background_color = self._theme.btn_background_color
            outline_color = self._theme.btn_outline_color
            text_surface = self._rendered_text_surface

        pygame.draw.rect(draw_surface, background_color, background_rect, border_radius=self._theme.btn_border_radius)
        if self._theme.btn_outline_color != None:
            pygame.draw.rect(draw_surface, outline_color, background_rect, width=self._theme.btn_outline_width, border_radius=self._theme.btn_border_radius)
        
        text_coordinates = pygame.Vector2(coordinates)
        text_coordinates.x += self.width / 2 - text_surface.get_width() / 2
        text_coordinates.y += self.height / 2 - text_surface.get_height() / 2

        draw_surface.blit(text_surface, text_coordinates)

        self.last_coordinates = coordinates
        if self._first_draw:
            self._first_draw = False