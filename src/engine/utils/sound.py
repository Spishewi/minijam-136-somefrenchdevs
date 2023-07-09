import pygame.mixer

pygame.mixer.init()

BUTTON_SOUND = pygame.mixer.Sound('./assets/sounds/zipclick.ogg')

DAMAGE_SOUND = pygame.mixer.Sound("./assets/sounds/Explosion2__006.ogg")

GAME_OVER_SOUND = pygame.mixer.Sound("./assets/sounds/Explosion3__010.ogg")

PLACE_TOWER_SOUND = pygame.mixer.Sound("./assets/sounds/Bass Drum__001.ogg")

_sounds_list = [
    BUTTON_SOUND,
    DAMAGE_SOUND,
    GAME_OVER_SOUND,
    PLACE_TOWER_SOUND
]

def set_sound_volume(volume: float) -> None:
    for sound in _sounds_list:
        sound.set_volume(volume)