from util import Stack
from random import choice


def traverse_graph(world):
    trail = Stack()

    visited = set()
    has_unexplored_paths = { world.starting_room.id }

    path = []
    trail.push((None, world.starting_room))

    # while there is at least one known room with paths that we have not traversed, keep traversing
    while len(has_unexplored_paths):
        current = trail.peek()[1]
        visited.add(current.id)

        # get every connecting room that we have not yet been to
        unvisited_neighbors = [n for n in get_neighbors(current) if n[1].id not in visited]
        # print(f'U_N: {[(n[0], n[1].id) for n in unvisited_neighbors]}')

        # this room has, at most, 1 neighbor that we have not yet visited.
        # therefore, everything about this room has been explored
        # this first 'if' is for tracking when the graph has been fully explored, not for traversing it
        if current.id in has_unexplored_paths and len(unvisited_neighbors) < 2:
            has_unexplored_paths.remove(current.id)

        # there is at least 1 neighbor of this room that we have not yet visited.
        # need to pick one and advance to it
        if len(unvisited_neighbors) > 0:
            # pick a neighbor
            direction, next_room = choice(unvisited_neighbors)

            # add it to the unexplored set (we haven't been yet, so we won't know if it has unexplored paths until we arrive)
            has_unexplored_paths.add(next_room.id)

            # add the direction to it to our traveral path
            path.append(direction)

            # add it to our backtracking trail
            # Yes, I unpacked a tuple just to repack it. No, I'm not sorry.
            trail.push((direction, next_room))

        # there are no neighbors, or they have all been visited.
        # effectively, this is a dead end. go back to the previous room
        else:
            # figure out which way is backwards, and record it, and remove the current room from our 'trail'
            path.append(invert_dir(trail.pop()[0]))

    return path


def get_neighbors(node):
    return [(d, node.get_room_in_direction(d)) for d in node.get_exits()]


def invert_dir(direction):
    if direction == 'n':
        return 's'
    elif direction == 's':
        return 'n'
    elif direction == 'e':
        return 'w'
    elif direction == 'w':
        return 'e'
    else:
        raise Exception('THAT\'S NOT A DIRECTION, WHAT DID YOU DO?!?')
