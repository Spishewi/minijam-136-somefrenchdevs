import pygame.event

SCENE_QUIT = pygame.event.custom_type()
"""
This event must be triggered when we wants to quit the game
"""

SCENE_SET = pygame.event.custom_type()
"""
This event must be triggered when we wants to change/set a scene
"""

SCENE_SET_LOADINGSCREEN = pygame.event.custom_type()
"""
This event must be triggered when we wants to activate the loading screen
"""

SCENE_REMOVE_LOADINGSCREEN = pygame.event.custom_type()
"""
This event must be triggered when we wants to remove the loading screen
"""

SCENE_TRANSITION_IN = pygame.event.custom_type()
"""
This event must be triggered to do a transition in
"""

SCENE_TRANSITION_OUT = pygame.event.custom_type()
"""
This event must be triggered to do a transition out
"""

SCENE_LOADING_ERROR = pygame.event.custom_type()
"""
This event must be triggered when a loading error is occured
"""

SCENE_GAME_LAUNCH = pygame.event.custom_type()
"""
This event must be triggered when a we want to lauch the game scene without a new save
"""

SCENE_NEW_GAME_LAUNCH = pygame.event.custom_type()
"""
This event must be triggered when a we want to lauch the game scene with a new save
"""
def scene_error_wrapper(callback, *args, **kwargs):
    try:
        callback(*args, **kwargs)
    except Exception as e:
        pygame.event.post(pygame.event.Event(SCENE_LOADING_ERROR, {"error" : e}))
        