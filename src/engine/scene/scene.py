from threading import Thread
import pygame.event
from engine.scene.scene_event import *

class Scene():
    """
    This is the base object to create a scene which implements async loading.
    """
    def __init__(self):
        """
        Initialise a scene
        """
        self.is_loaded = False
            
    @staticmethod
    def load_decorator(function):
        """
        decorator to put before the scene load function of the scene
        (this makes the loading asyncronized)
        """

        def decorator(*args, **kwargs):
            def thread_function():
                # tell the scene manager to set the loading screen to on
                pygame.event.post(pygame.event.Event(SCENE_SET_LOADINGSCREEN))
                # execute the loading
                function(*args, **kwargs)
                # the first argument is "self"
                # tell the game that the scene is fully loaded
                args[0].is_loaded = True
                # tell the scene manager to remove the loading screen
                pygame.event.post(pygame.event.Event(SCENE_REMOVE_LOADINGSCREEN))
            
            thread = Thread(target=scene_error_wrapper, args=(thread_function,))
            thread.start()

        return decorator

    @staticmethod
    def update_decorator(function):
        """
        decorator which decorate the update function.
        The update function will be ignored at each call if the scene isn't fully loaded.
        """
        def decorator(*args, **kwargs):
            if args[0].is_loaded:
                function(*args, **kwargs)
        return decorator
    @staticmethod
    def draw_decorator(function):
        """
        decorator which decorate the draw function.
        The draw function will be ignored at each call if the scene isn't fully loaded.
        """
        def decorator(*args, **kwargs):
            if args[0].is_loaded:
                function(*args, **kwargs)
        return decorator
    @staticmethod
    def event_handler_decorator(function):
        """
        decorator which decorate the event_handler.
        The event_handler will be ignored at each call if the scene isn't fully loaded.
        """
        def decorator(*args, **kwargs):
            if args[0].is_loaded:
                function(*args, **kwargs)
        return decorator
    
    @staticmethod
    def map_set_decorator(function):
        """
        decorator which decorate the event_handler.
        The event_handler will be ignored at each call if the scene isn't fully loaded.
        """
        def decorator(*args, **kwargs):
            if args[0].is_loaded:
                function(*args, **kwargs)
        return decorator