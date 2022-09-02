from __future__ import annotations
from typing import Iterator, Tuple, List, TYPE_CHECKING
from game_map import GameMap


import tile_types
import tcod
import random
import entity_factories

if TYPE_CHECKING: 
    from entity import Entity


class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y
    
    @property
    def inner(self) -> Tuple[slice, slice]:
        """returns the inner area of the room as a 2d array index"""
        return slice(self.x1 +1, self.x2), slice(self.y1 +1, self.y2) 

    def intersects(self, other: RectangularRoom) -> bool :
        """return true if the room overlaps with another rectangularRoom"""
        return (
            self.x1 <= other.x2
            and self.x2 >= other.x1
            and self.y1 <= other.y2
            and self.y2 >= other.y1
        )

def generate_dungeon(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    max_monsters_per_room: int,
    player: Entity,
    ) -> GameMap:
    """generate a new dungeon map"""
    dungeon = GameMap(map_width,map_height, entities=[player])

    rooms : List[RectangularRoom] = []

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        x = random.randint(0, dungeon.width - room_width -1)
        y = random.randint(0, dungeon.height - room_height -1)

        # RectangularRoom class makes rectangles
        new_room = RectangularRoom(x, y, room_width, room_height)

        #check if this room intersects with any other room
        if any(new_room.intersects(other_room) for other_room in rooms):
            continue #skip this room and make a new one

        #if there is no intersetions the room is valid

        #dig out the room in his area
        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:
            #this is the first room where the player starts
            player.x, player.y = new_room.center
        else: #all other rooms
            #dig a tunnel between this room and the previous
            for x, y in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x,y] = tile_types.floor

        place_entities(new_room, dungeon, max_monsters_per_room)
        # finally we append the new room to the list
        rooms.append(new_room)

    return dungeon


def place_entities(
    room: RectangularRoom,
    dungeon: GameMap, 
    max_monsters: int) -> None:

    number_of_monsters = random.randint(0, max_monsters)
    
    for i in range(number_of_monsters):
        x = random.randint(room.x1 + 1, room.x2 -1)
        y = random.randint(room.y1 + 1, room.y2 -1)

        if not any(entity.x == x and entity.y == y for entity in dungeon.entities):
            if random.random() < 0.8:
                entity_factories.orc.spawn(dungeon, x, y)
            else:
                entity_factories.troll.spawn(dungeon, x, y)






def tunnel_between(
    start: Tuple[int, int], end: Tuple[int, int]
    ) -> Iterator[Tuple[int, int]]:
    """return an L-shaped tunnel based on two points"""
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5: # 50%
        #move horizontally, then vertically
        corner_x, corner_y = x2, y1
    else:
        #move vertically, then horizontally
        corner_x, corner_y = x1, y2
        
        # Generate the coordinates for this tunnel.
    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y

