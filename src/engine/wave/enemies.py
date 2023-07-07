import pygame, pytmx

from engine.utils.animations import EnemyAnimation
from debug import debug

class Enemy:
    def __init__(self, spawn: pytmx.TiledObject, level: int, map_manager, health_factor: float, speed: float, animation_path: str) -> None:
        self.map: pytmx.TiledMap = map_manager.get_current_map()
        self.health = health_factor * level
        self.speed = speed
        self.position = pygame.Vector2(spawn.x, spawn.y)
        self.goal = self.map.get_object_by_id(spawn.properties['next'])
        self.animation = EnemyAnimation(animation_path)
        self.velocity = pygame.Vector2()
        self.old_goal = spawn
        self.pos_to_goal = pygame.Vector2(1, 1)
        
    def move(self, dt: float):
        goal_pos = pygame.Vector2(self.goal.x, self.goal.y)
        self.pos_to_goal = goal_pos - self.position
        pos_to_goal_distance = self.pos_to_goal.magnitude()
        forward_distance = self.speed * dt
        
        
        if pos_to_goal_distance >= forward_distance:
            self.velocity = self.pos_to_goal.normalize() * forward_distance
            self.pos_to_goal -= self.velocity

        else:
            self.position = goal_pos
            try:
                self.old_goal = self.goal
                self.goal = self.map.get_object_by_id(self.goal.properties['next'])
            except KeyError:
                self.goal = None
            else:
                goal_pos = pygame.Vector2(self.goal.x, self.goal.y)
                self.pos_to_goal = goal_pos - self.position
                
                self.velocity = self.pos_to_goal.normalize() * (forward_distance - pos_to_goal_distance) # ici pos_to_goal_distance est l'ancienne
        debug.add(f'velocity: {self.velocity}')
        self.position += self.velocity
            
    def draw(self, draw_surface: pygame.Surface):
        animation = self.animation.get_curent_animation(self.velocity)
        draw_surface.blit(animation, self.position - pygame.Vector2(animation.get_width() / 2, animation.get_height()))
    
    def update(self, dt: float):
        self.move(dt)
        
        if self.goal == None :
            return self.health
        return 0
    

class Skeleton(Enemy):
    def __init__(self, spawn: pytmx.TiledObject, level: int, map_manager) -> None:
        super().__init__(
            spawn, 
            level, 
            map_manager,
            health_factor = 1,
            speed = 12,
            animation_path = '../assets/enemies/skeleton')
        
class Goblin(Enemy):
    def __init__(self, spawn: pytmx.TiledObject, level: int, map_manager) -> None:
        super().__init__(
            spawn, 
            level, 
            map_manager,
            health_factor = 1,
            speed = 15,
            animation_path = '../assets/enemies/goblin')
        
class Mushroom(Enemy):
    def __init__(self, spawn: pytmx.TiledObject, level: int, map_manager) -> None:
        super().__init__(
            spawn, 
            level, 
            map_manager,
            health_factor = 1,
            speed = 8,
            animation_path = '../assets/enemies/mushroom')
        

class Slime(Enemy):
    def __init__(self, spawn: pytmx.TiledObject, level: int, map_manager) -> None:
        super().__init__(
            spawn, 
            level, 
            map_manager,
            health_factor = 1,
            speed = 5,
            animation_path = '../assets/enemies/slime')