import pygame, pytmx, math, random

from engine.wave.enemies import Enemy, Skeleton, Goblin, Mushroom, Slime
from engine.utils.life_bar import LifeBar

ENEMIES_TYPES = [Skeleton, Goblin, Mushroom, Slime]

class WaveManager:
    MAX_VILLAGE_LIFE = 1000
    def __init__(self, map_manager: pytmx.TiledMap) -> None:
        self.map_manager = map_manager
        map = map_manager.get_current_map()
        self.spawn = map.get_object_by_name('0')
        self.enemies: list[Enemy] = []
        self.village_health = WaveManager.MAX_VILLAGE_LIFE
        
        self.wave_nb = 0
        self.last_throw = -500
        self.start_new_wave()

        self.custom_ticks = 0
        self.time_for_next_throw = 0
        
        self.life_bar = LifeBar(pygame.Vector2(8, 8), 20, 5)
    
    def event_handler(self, event: pygame.Event):
        ...

    
    def draw(self, draw_surface: pygame.Surface):
        for enemy in sorted(self.enemies, key=lambda enemy: enemy.position.y):
            enemy.draw(draw_surface)

        if len(self.enemies) > 0:
            pygame.draw.circle(draw_surface, (255, 255, 255), self.enemies[0].position, radius=5)
            
        self.life_bar.draw()
    
    def update(self, dt: float):
        self.custom_ticks += dt
        for i, enemy in enumerate(self.enemies):
            pv_to_remove = enemy.update(dt)
            
            if pv_to_remove != 0:
                self.damage_village(pv_to_remove)
                self.enemies.pop(i)
        
        if self.enemies_to_throw != 0 and self.custom_ticks > self.time_for_next_throw:
            self.enemies.append(random.choice(ENEMIES_TYPES)(self.spawn, self.wave_nb, self.map_manager))
            #self.enemies.append(Slime(self.spawn, self.wave_nb, self.map_manager))
            self.enemies_to_throw -= 1
            self.custom_ticks = 0
            self.time_for_next_throw = random.random() * 1.5 + 1.5 # entre 1.5 sec et 3 sec
                
        if len(self.enemies) == 0 and self.enemies_to_throw == 0:
            self.start_new_wave()

        self._sort_enemies()
    
    def draw_ui(self, draw_surface):
        pass
    
    def start_new_wave(self):
        self.wave_nb += 1
        self.enemies_to_throw = math.ceil(self.wave_nb*0.65)
    
    def damage_village(self, damages: int):
        self.village_health -= damages
    
    def _sort_enemies(self) -> None:
        tmp = {}
        for enemy in self.enemies:
            goal_number = int(enemy.goal.name)
            if goal_number in tmp.keys():
                tmp[goal_number].append(enemy)
            else:
                tmp[goal_number] = [enemy]
        
        tmp2 = sorted(list(tmp.items()), key=lambda x: x[0], reverse=True)
        
        for i in range(len(tmp2)):
            tmp2[i][1].sort(key=lambda x: (x.pos_to_goal.magnitude()/(pygame.Vector2(x.goal.x, x.goal.y) - pygame.Vector2(x.old_goal.x, x.old_goal.y)).magnitude()))
        
        tmp3 = [enemy[1] for enemy in tmp2]

        tmp4 = []
        for i in tmp3:
            tmp4.extend(i)

        self.enemies = tmp4