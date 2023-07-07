from __future__ import annotations
from collections import namedtuple

import pygame
import math

from engine.fixed_ui.fixed_widget import Widget
from engine.utils.enumerations import AnchorX, AnchorY, Orientation
from engine.utils.hitbox import RectangularHitbox

from engine.fixed_ui.widgets.slider import Slider
from engine.fixed_ui.widget_theme import Widget_theme

from engine.utils.settings import user_settings

from debug import debug

Place_widget = namedtuple('Place_widget', ['widget', 'x', 'y', 'anchor'])
Grid_widget = namedtuple('Grid_widget', ['widget', 'row', 'column', 'anchor', 'row_span', 'col_span'])
List_widget = namedtuple('List_widget', ['widget', 'margin_x', 'margin_y', 'anchor_x'])
Anchor = namedtuple('Anchor', ['x', 'y'])

scrollbar_theme = Widget_theme(
    font_path = "../assets/font/PublicPixel.ttf",
    text_color = pygame.Color(255, 255, 255),
    hovered_text_color = pygame.Color(150, 200, 250),

    btn_background_color = pygame.Color(200, 200, 200),
    btn_hovered_background_color = pygame.Color(75, 125, 175),
    btn_outline_color = pygame.Color(255, 255, 255),
    btn_hovered_outline_color = pygame.Color(125, 175, 225),
    btn_border_radius = 3,
    btn_outline_width = 2,
    btn_padding = 5,

    check_width = 3,
    check_color = pygame.Color(153, 255, 147),

    slider_bar_color = pygame.Color(50, 75, 100),
    slider_bar_width = 3,
    slider_btn_width = 10
)

class Frame():
    UNIQUE_ID = 0

    def __init__(self, width: int = None, height: int = None, scrollable: bool = False) -> None:
        self._grid_row = None
        self._grid_column = None

        self._widgets: dict[int, Place_widget | Grid_widget] = {}

        self.width = width
        self.height = height

        self.scrollable = scrollable
        self.scroll: int = 0
        self.need_scrollbar = False

        if self.scrollable:
            if self.height != None:
                self.scrollbar = Slider(scrollbar_theme, 10, self.height - scrollbar_theme.slider_btn_width * 2, 0, Orientation.VERTICAL)
            else:
                self.scrollbar = Slider(scrollbar_theme, 10, scrollbar_theme.slider_btn_width * 2, 0, Orientation.VERTICAL)

        self.needed_width = 0
        self.needed_height = 0

        self.background_surface = None
        self.background_surface_opacity = 0

        self.last_coordinates = None
        self.hovered = False

        self.list_position = 0

    def _update_scrollbar(self):
        self.scrollbar._width = 10
        self.scrollbar._height = self.height - scrollbar_theme.slider_btn_width * 2

    def set_background(self, opacity: float = 0):
        self.background_surface_opacity = opacity * 255
        self.background_surface = None

    def draw(self, draw_surface: pygame.Surface, coordinates: pygame.Vector2() = None) -> None:
        """
        Draw all widgets on `draw_surface`
        """

        self.list_position = 0

        if self.height == None or self.width == None:
            if self.height == None:
                self.height = draw_surface.get_height()
            if self.width == None:
                self.width = draw_surface.get_width()
            if self.scrollable:
                self._update_scrollbar()

        if self.background_surface_opacity != 0:
            if self.background_surface == None or self.background_surface.get_size() != (self.width, self.height):
                self.background_surface = pygame.Surface((self.width, self.height))
                self.background_surface.fill((self.background_surface_opacity,)*3)


            if coordinates == None:
                coordinates = pygame.Vector2(0, 0)
            
            draw_surface.blit(self.background_surface, coordinates, special_flags=pygame.BLEND_MULT)



        for widget in self._widgets.values():
            if isinstance(widget, Grid_widget):
                rect = self._draw_grid(widget, draw_surface)
            
            elif isinstance(widget, Place_widget):
                rect = self._draw_place(widget, draw_surface)
            
            elif isinstance(widget, List_widget):
                rect = self._draw_list(widget, draw_surface)

            # On recalcul la taille maximum requise, pour le scroll
            if rect.bottomright[0] > self.needed_width:
                self.needed_width = rect.bottomright[0]
            if rect.bottomright[1] > self.needed_height:
                self.needed_height = rect.bottomright[1]

        if self.scrollable and self.need_scrollbar:
            x = self.width - self.scrollbar.width // 2 - self.scrollbar._theme.slider_btn_width
            y = self.scrollbar._theme.slider_btn_width
            self.scrollbar.draw(pygame.Vector2(x, y), draw_surface)

        self.last_coordinates = coordinates
        #pygame.draw.rect(draw_surface, (255, 0, 0), (0, 0, self.width, self.height), width=1)

    def _draw_list(self, widget: List_widget, draw_surface: pygame.Surface) -> pygame.Rect:
        """
        affiche le widget en utilisant le gestionnaire de liste.
        retourne sa boite de collision (pygame.Rect)
        """

        width, height = draw_surface.get_size()
        coordinates = pygame.Vector2()

        if widget.anchor_x == AnchorX.LEFT:
            coordinates.x = widget.margin_x
        elif widget.anchor_x == AnchorX.CENTER:
            coordinates.x = (width - widget.widget.width)/2
        else: # RIGHT
            coordinates.x = width - widget.widget.width - widget.margin_x





        coordinates.y = widget.margin_y + self.list_position
        self.list_position += widget.widget.height + widget.margin_y * 2



        if isinstance(widget.widget, Frame):
            raise ValueError("Frames cannot be listed !")

        if coordinates.x <= width and coordinates.y  - self.scroll <= height:
            widget.widget.draw(coordinates=pygame.Vector2(coordinates.x, coordinates.y - self.scroll), draw_surface=draw_surface)
        
        return pygame.rect.Rect(coordinates.x, coordinates.y, widget.widget.width + widget.margin_x, widget.widget.height + widget.margin_y)


    def _draw_grid(self, widget: Grid_widget, draw_surface: pygame.Surface) -> pygame.Rect:
        """
        affiche le widget en utilisant le gestionnaire de grille.
        retourne sa boite de collision (pygame.Rect)
        """
        if self._grid_column == None or self._grid_row == None:
            return
        
        width, height = draw_surface.get_size()
        coordinates = pygame.Vector2()

        col_width = width/self._grid_column
        row_height = height/self._grid_row

        # DEFAULT TOP-LEFT
        debug.add(f"{widget.col_span}, {widget.row_span}")
        coordinates.x = (col_width)*(widget.column )
        coordinates.y = (row_height)*(widget.row)


        if isinstance(widget.widget, Frame):
            rect = pygame.Rect(coordinates.x, coordinates.y, 0, 0)

            widget.widget.width = col_width * widget.col_span
            widget.widget.height = row_height * widget.row_span

            rect.width = widget.widget.width
            rect.height = widget.widget.height
            draw_surface = draw_surface.subsurface(rect)

            widget.widget._width = rect.width

            widget.widget._height = rect.height
            widget.widget._update_scrollbar()
        else:
            coordinates.x += (col_width) *  (widget.col_span-1) / 2
            coordinates.y += (row_height) *  (widget.row_span-1) / 2

            
            if widget.anchor.x == AnchorX.CENTER:
                coordinates.x += (col_width - widget.widget.width) / 2
            elif widget.anchor.x == AnchorX.RIGHT:
                coordinates.x += (col_width - widget.widget.width)

            if widget.anchor.y == AnchorY.CENTER:
                coordinates.y += (row_height - widget.widget.height) / 2
            elif widget.anchor.y == AnchorY.BOTTOM:
                coordinates.y += (row_height - widget.widget.height)


        if coordinates.x <= width and coordinates.y  - self.scroll <= height:
            widget.widget.draw(coordinates=pygame.Vector2(coordinates.x, coordinates.y - self.scroll), draw_surface=draw_surface)
        
        return pygame.rect.Rect(coordinates.x, coordinates.y, widget.widget.width, widget.widget.height)

    def _draw_place(self, widget: Place_widget, draw_surface: pygame.Surface) -> pygame.Rect:
        """
        affiche le widget aux coordonnées demandées.
        retourne sa boite de collision (pygame.Rect)
        """
        width, height = draw_surface.get_size()
        coordinates = pygame.Vector2()
        coordinates.x = widget.x
        coordinates.y = widget.y

        if widget.anchor.x == AnchorX.CENTER:
            coordinates.x -= widget.widget.width / 2
        elif widget.anchor.x == AnchorX.RIGHT:
            coordinates.x -= widget.widget.width

        if widget.anchor.y == AnchorY.CENTER:
            coordinates.y -= widget.widget.height / 2
        elif widget.anchor.y == AnchorY.BOTTOM:
            coordinates.y -= widget.widget.height

        if isinstance(widget.widget, Frame):
            rect = pygame.Rect(coordinates.x, coordinates.y, 0, 0)
            rect.width = widget.widget.width
            rect.height = widget.widget.height
            draw_surface = draw_surface.subsurface(rect)

            widget.widget._width = rect.width
            widget.widget._height = rect.height
            widget.widget._update_scrollbar()

        if coordinates.x <= width and coordinates.y  - self.scroll <= height:
            widget.widget.draw(coordinates=pygame.Vector2(coordinates.x, coordinates.y - self.scroll), draw_surface=draw_surface)

        return pygame.rect.Rect(coordinates.x, coordinates.y, widget.widget.width, widget.widget.height)

    def update(self, dt: float) -> None:
        for widget in self._widgets.values():
            widget.widget.update(dt)

        if self.scrollable:
            self.scrollbar.update(dt)
            if self.height != None:
                self.need_scrollbar = self.needed_height > self.height

    def event_handler(self, event: pygame.event.Event) -> None:

        for widget in self._widgets.values():
            widget.widget.event_handler(event)

        if self.scrollable and self.need_scrollbar:
            self.scrollbar.event_handler(event)
            self.scroll = max(1, self.needed_height - self.height) * self.scrollbar.value

            if event.type == pygame.MOUSEMOTION:
                if self.last_coordinates == None:
                    return

                hitbox = RectangularHitbox(self.last_coordinates, self.width, self.height)
                self.hovered = hitbox.collide_point(pygame.Vector2(event.pos))

            elif event.type == pygame.MOUSEWHEEL and self.hovered:
                scroll_in_px = max(1, self.needed_height - self.height)
                scroll_value = (self.scroll - event.precise_y * user_settings.mouse.scroll_speed) / scroll_in_px
                if scroll_value < 0:
                    scroll_value = 0
                elif scroll_value > 1:
                    scroll_value = 1

                self.scrollbar.value = scroll_value

    def list(self, widget, margin_x: int = 0, margin_y: int = 0, anchor_x: AnchorX = AnchorX.LEFT) -> int:
        list_widget = List_widget(widget, margin_x, margin_y, anchor_x)

        widget_id = self._get_unique_id()
        self._widgets[widget_id] = list_widget
        return widget_id

    def grid(self, widget, row: int, column: int, anchor: tuple[AnchorX, AnchorY] = (AnchorX.LEFT, AnchorY.TOP), row_span = 1,column_span = 1) -> int:
        grid_widget = Grid_widget(widget, row, column, Anchor(anchor[0], anchor[1]), row_span, column_span)
        widget_id = self._get_unique_id()
        self._widgets[widget_id] = grid_widget
        return widget_id

    def place(self, widget, coordinates: pygame.Vector2, anchor: tuple[AnchorX, AnchorY] = (AnchorX.LEFT, AnchorY.TOP)) -> int:
        """
        Place a widget somewhere
        """
        place_widget = Place_widget(widget, coordinates.x, coordinates.y, Anchor(anchor[0], anchor[1]))
        widget_id = self._get_unique_id()
        self._widgets[widget_id] = place_widget
        return widget_id

    def grid_configure(self, row: int = None, column: int = None) -> None:
        """
        Configure the grid size used for grided widgets
        """
        if row != None:
            self._grid_row = row
        if column != None:
            self._grid_column = column

    def remove(self, widget_id: int) -> None:
        """
        Remove a widget from the UI
        """
        del self._widgets[widget_id]

    def clear(self) -> None:
        self._widgets = {}

    def _get_unique_id(self) -> int:
        Frame.UNIQUE_ID += 1
        return Frame.UNIQUE_ID
