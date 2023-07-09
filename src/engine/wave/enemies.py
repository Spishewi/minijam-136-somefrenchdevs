import pygame, pytmx

from engine.utils.animations import EnemyAnimation
from engine.utils.life_bar import LifeBar
from debug import debug

class Enemy:
    def __init__(self, spawn: pytmx.TiledObject, level: int, map_manager, health_factor: float, speed: float, animation_path: str) -> None:
        self.map: pytmx.TiledMap = map_manager.get_current_map()
        self.start_health = health_factor * level
        self.health = self.start_health
        self.speed = speed
        self.position = pygame.Vector2(spawn.x, spawn.y)
        self.goal = self.map.get_object_by_id(spawn.properties['next'])
        self.animation = EnemyAnimation(animation_path)
        self.velocity = pygame.Vector2()
        self.old_goal = spawn
        self.pos_to_goal = pygame.Vector2(1, 1)
        self.must_be_deleted = False
        
        self.height = self.animation.get_curent_animation(self.velocity).get_height()
        self.width = self.animation.get_curent_animation(self.velocity).get_width()
        self.life_bar = LifeBar(self.position + pygame.Vector2(0, -self.height-2), 10, 3)
        
    def get_center(self):
        return self.position + pygame.Vector2(0, -self.height/2)
        
    def move(self, dt: float):
        forward_distance = self.speed * dt
        
        while forward_distance > 0:
            goal_pos = pygame.Vector2(self.goal.x, self.goal.y)
            self.pos_to_goal = goal_pos - self.position
            pos_to_goal_distance = self.pos_to_goal.magnitude()

            if pos_to_goal_distance >= forward_distance:
                self.velocity = self.pos_to_goal.normalize() * forward_distance
                self.pos_to_goal -= self.velocity
                forward_distance = 0
                self.position += self.velocity

            else:
                self.position = goal_pos
                forward_distance -= pos_to_goal_distance
                try:
                    self.old_goal = self.goal
                    self.goal = self.map.get_object_by_id(self.goal.properties['next'])
                except KeyError:
                    self.goal = None
                    break

                    
                
            
    def draw(self, draw_surface: pygame.Surface):
        animation = self.animation.get_curent_animation(self.velocity)
        draw_surface.blit(animation, self.position - pygame.Vector2(animation.get_width() / 2, animation.get_height()))
        
        if self.health/self.start_health < 1:
            self.life_bar.draw(draw_surface, self.health/self.start_health)
    
    def update(self, dt: float):
        self.move(dt)
        
        self.life_bar.update(self.position + pygame.Vector2(0, -self.height-2))
        
        if self.goal == None :
            return self.health
        return 0
    

class Skeleton(Enemy):
    def __init__(self, spawn: pytmx.TiledObject, level: int, map_manager) -> None:
        super().__init__(
            spawn, 
            level, 
            map_manager,
            health_factor = 8,
            speed = 17,
            animation_path = './assets/enemies/skeleton')
        
class Goblin(Enemy):
    def __init__(self, spawn: pytmx.TiledObject, level: int, map_manager) -> None:
        super().__init__(
            spawn, 
            level, 
            map_manager,
            health_factor = 5,
            speed = 20,
            animation_path = './assets/enemies/goblin')
        
class Mushroom(Enemy):
    def __init__(self, spawn: pytmx.TiledObject, level: int, map_manager) -> None:
        super().__init__(
            spawn, 
            level, 
            map_manager,
            health_factor = 12,
            speed = 13,
            animation_path = './assets/enemies/mushroom')
        

class Slime(Enemy):
    def __init__(self, spawn: pytmx.TiledObject, level: int, map_manager) -> None:
        super().__init__(
            spawn, 
            level, 
            map_manager,
            health_factor = 15,
            speed = 10,
            animation_path = './assets/enemies/slime')