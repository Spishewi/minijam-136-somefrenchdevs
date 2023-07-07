# std import
import sys
import pygame

# nos propre fichier import
from engine.scene.scene_manager import SceneManager
from engine.utils.settings import dev_settings

if __name__ == "__main__":
    # on lance le jeu

    scene_manager = SceneManager()
    scene_manager.run()

    # on ferme correctement pygame et python
    pygame.quit()
    sys.exit()