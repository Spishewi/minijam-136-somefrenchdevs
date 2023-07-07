from __future__ import annotations

# std import
import pygame
import math


def raycast(map, start: pygame.Vector2, end_or_direction: pygame.Vector2, start_to_end: bool = True, max_length: float = 0.0, solide: bool = True, layer_name: str = "floor") -> tuple[pygame.Vector2]:
    """
    fonction de raycast avec soit :
        - start to end (tiled based) 
        - start (tiled based) avec direction (normalized) et length (tiled based) 
    
        - solide (bool) pour savoir si on veut l'air ou le solide 
        - layer_name

    RETURN -> tuple de vecteurs :
        - coordonnées de l'intersection
        - coordonnées de la tile intersectée

    OU -> None:
        - si erreur ou pas d'intersection
    """

    # setup variables and const
    if max_length < 0:
        max_distance = - max_length
    else:
        max_distance = max_length


    if start_to_end:

        v_start_to_end = end_or_direction - start
        
        if v_start_to_end != pygame.Vector2(0,0):
            direction = v_start_to_end.normalize()
        else:
            return None

        if max_length == 0.0:
            max_distance = v_start_to_end.magnitude()
        
    else:      
        direction = end_or_direction
        
    ray_unit_step_size = pygame.Vector2()


    if direction.x != 0 and direction.y != 0:
        ray_unit_step_size.x = math.sqrt(1 + (direction.y / direction.x) ** 2)
        ray_unit_step_size.y = math.sqrt(1 + (direction.x / direction.y) ** 2)
    else:
        return None
    
    ray_start = start
    map_check = pygame.Vector2(int(ray_start.x), int(ray_start.y))
    ray_length_1d = pygame.Vector2()
    step = pygame.Vector2()

    if direction.x < 0:
        step.x = -1
        ray_length_1d.x = (ray_start.x - map_check.x) * ray_unit_step_size.x
    else:
        step.x = 1
        ray_length_1d.x = (map_check.x + 1 - ray_start.x) * ray_unit_step_size.x

    if direction.y < 0:
        step.y = -1
        ray_length_1d.y = (ray_start.y - map_check.y) * ray_unit_step_size.y
    else:
        step.y = 1
        ray_length_1d.y = (map_check.y + 1 - ray_start.y) * ray_unit_step_size.y

    map_layer = map.get_layer_by_name(layer_name)
    distance = 0
    
    min_x = 0
    min_y = 0
    max_x = map.width - 1
    max_y = map.height - 1

    """
    test for edge cases on the first loop
    """
    temp_map_check = start.copy() + step/4

    if min_y <= map_check.y <= max_y and min_x <= map_check.x <= max_x:
        if solide:
            if map_layer.data[int(temp_map_check.y)][int(temp_map_check.x)] != 0:
                tile_intersection_pos = pygame.Vector2(int(temp_map_check.x), int(temp_map_check.y))
                return (ray_start, tile_intersection_pos) # (coordonnées de l'intersection, coordonnées de la tile intersectée)
        else:
            if map_layer.data[int(temp_map_check.y)][int(temp_map_check.x)] == 0:
                tile_intersection_pos = pygame.Vector2(int(temp_map_check.x), int(temp_map_check.y))
                return (ray_start, tile_intersection_pos) # (coordonnées de l'intersection, coordonnées de la tile intersectée)
    """
    Main loop
    """
    while distance < max_distance and min_y <= map_check.y <= max_y and min_x <= map_check.x <= max_x:

        if solide:
            if map_layer.data[int(map_check.y)][int(map_check.x)] != 0:
                intersection = ray_start + direction * distance
                if distance != 0:
                    return (intersection, map_check.copy()) # (coordonnées de l'intersection, coordonnées de la tile intersectée)
        else:
            if map_layer.data[int(map_check.y)][int(map_check.x)] == 0:
                intersection = ray_start + direction * distance
                if distance != 0:
                    return (intersection, map_check.copy()) # (coordonnées de l'intersection, coordonnées de la tile intersectée)

        if ray_length_1d.x < ray_length_1d.y:
            map_check.x += step.x
            distance = ray_length_1d.x
            ray_length_1d.x += ray_unit_step_size.x
        else:
            map_check.y += step.y
            distance = ray_length_1d.y
            ray_length_1d.y += ray_unit_step_size.y


    return None