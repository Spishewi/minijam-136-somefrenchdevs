from __future__ import  annotations
from engine.utils.hitbox import RectangularHitbox, Hitbox
from objects.game_object import GameObject
from collections import namedtuple

TreeItem = namedtuple('TreeItem', ['hitbox', 'game_object'])

class QuadTree:
    CAPACITY = 4

    def __init__(self, boundary: RectangularHitbox) -> None:
        self.container: list[TreeItem] = []
        self.boundary = boundary
        self.divided = False

    def _divide(self):
        NW_hitbox = RectangularHitbox(self.boundary.pos, self.boundary.width/2, self.boundary.height/2)
        self.NW = QuadTree(NW_hitbox)
        NE_hitbox = RectangularHitbox(self.boundary.pos, self.boundary.width/2, self.boundary.height/2)
        self.NE = QuadTree(NE_hitbox)
        SW_hitbox = RectangularHitbox(self.boundary.pos, self.boundary.width/2, self.boundary.height/2)
        self.SW = QuadTree(SW_hitbox)
        SE_hitbox = RectangularHitbox(self.boundary.pos, self.boundary.width/2, self.boundary.height/2)
        self.SE = QuadTree(SE_hitbox)

    def _append(self, game_object: GameObject) -> None:
        """
        append the object in this node
        """
        self.container.append(TreeItem(game_object.get_hitbox().copy(), game_object))

    def remove(self, current_hitbox: Hitbox, game_object: GameObject) -> None:
        for tree_item in self.container:
            if tree_item.game_object is game_object:
                #print(tree_item.game_object, game_object)
                self.container.remove(tree_item)
                return True
        
        if self.divided:
            if self.NW.boundary.collide(current_hitbox):
                return self.NW.remove(game_object)
            if self.NE.boundary.collide(current_hitbox):
                return self.NE.remove(game_object)
            if self.SW.boundary.collide(current_hitbox):
                return self.SW.remove(game_object)
            if self.SE.boundary.collide(current_hitbox):
                return self.SE.remove(game_object)
    
    def update(self, current_hitbox: Hitbox, game_object: GameObject) -> None:
        self.remove(current_hitbox, game_object)
        self.append(game_object)

    def append(self, game_object: GameObject):
        """
        append an object in this tree (recusively)
        """
        obj_hitbox = game_object.get_hitbox()

        if len(self.container) < QuadTree.CAPACITY:
            self._append(game_object)
            return

        if not self.divided:
            self._divide()

        if self.NW.boundary.contains(obj_hitbox):
            self.NW.append(game_object)
        elif self.NE.boundary.contains(obj_hitbox):
            self.NE.append(game_object)
        elif self.SW.boundary.contains(obj_hitbox):
            self.SW.append(game_object)
        elif self.SE.boundary.contains(obj_hitbox):
            self.SE.append(game_object)
        else:
            self._append(game_object)

    def extend(self, game_objects: list[GameObject]) -> None:
        """
        append objects in this tree (recusively)
        """
        for game_object in game_objects:
            self.append(game_object)

    def query(self, search_boundary: RectangularHitbox) -> list[GameObject]:
        """
        query objects in this tree (recusively)
        """
        result_list = []

        for obj in self.container:
            try:
                if search_boundary.collide(obj.hitbox):
                    result_list.append(obj)
            except Exception as e:
                print(obj)
                raise e

        if self.divided:
            if self.NW.boundary.collide(search_boundary):
                result_list.extend(self.NW.query(search_boundary))
            if self.NE.boundary.collide(search_boundary):
                result_list.extend(self.NE.query(search_boundary))
            if self.SW.boundary.collide(search_boundary):
                result_list.extend(self.SW.query(search_boundary))
            if self.SE.boundary.collide(search_boundary):
                result_list.extend(self.SE.query(search_boundary))

        return result_list
    
    def all(self) -> list[GameObject]:
        """
        get all the tree's objects
        """
        result_list = []
        result_list.extend(self.container)

        if self.divided:
            result_list.extend(self.NW.all())
            result_list.extend(self.NE.all())
            result_list.extend(self.SW.all())
            result_list.extend(self.SE.all())
        return result_list
            