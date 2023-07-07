import pygame.event

GAME_SAVE = pygame.event.custom_type()
"""
This event must be triggered to save the game
"""

GAME_SAVE_AND_QUIT = pygame.event.custom_type()
"""
This event must be triggered to save and quit the game
"""