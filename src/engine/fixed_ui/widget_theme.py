from __future__ import annotations

import pygame
from copy import deepcopy

#from engine.fixed_ui.fixed_widget import Widget

class Undefined():
    __repr__ = __str__ = "Undefined"

class Widget_theme():
    def __init__(self, **kwargs) -> None:
        # if something is undefined, it's needed
        
        # default
        self.font_path = Undefined
        self.text_color = pygame.Color(255, 255, 255)
        self.hovered_text_color = None

        self.global_background = None

        # button
        self.btn_background_color = None
        self.btn_hovered_background_color = None
        self.btn_outline_color = None
        self.btn_hovered_outline_color = None
        self.btn_border_radius = 0
        self.btn_outline_width = 0
        self.btn_padding = 0

        # ckeckbox
        self.check_width = 1
        self.check_color = pygame.Color(255, 255, 255)

        # Slider
        self.slider_bar_color = pygame.Color(255, 255, 255)
        self.slider_bar_width = 1
        self.slider_btn_width = 10

        self.update(**kwargs)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key in dir(self):
                self.__setattr__(key, value)
            else:
                raise AttributeError(f"Attribute \"{key}\" not found")
            
    def __getattribute__(self, name: str):
        value = object.__getattribute__(self, name)
        if value == Undefined:
            raise AttributeError("This attribute hasn't been defined")
        return value

    def __str__(self) -> str:
        return str(self.__dict__)
    
    def __repr__(self) -> str:
        return str(self)
    
    def deepcopy(self) -> Widget_theme:
        return deepcopy(self)


if __name__ == "__main__":
    theme = Widget_theme()
    print(theme.font_path)

    theme.update(font_path="this")

    print(theme)
    print(theme.font_path)