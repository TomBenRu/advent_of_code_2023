import pickle


def main():
    grid = [list(line.strip("\n")) for line in open("input.txt", "r").readlines()]

    # pad grid for easier parsing
    for i in range(len(grid)):
        grid[i].append(".")
        grid[i].insert(0, ".")

    grid.append(list("." * len(grid[0])))
    grid.insert(0, list("." * len(grid[0])))

    tiles = [".", "-", "|", "7", "J", "L", "F"]

    # this 2D list encodes the direction you will end up facing after stepping
    # onto a specific type of tile from a specific direction
    # the first index represents the direction you enter from: 0,1,2,3 = NESW
    # the second index represents the type of tile, in the same order as the
    # list above
    tile_outputs = [
        [-1, -1, 0, 3, -1, -1, 1],
        [-1, 1, -1, 2, 0, -1, -1],
        [-1, -1, 2, -1, 3, 1, -1],
        [-1, 3, -1, -1, -1, 0, 2],
    ]

    # given a tile on the loop and the direction you are currently facing,
    # follow the loop until you end up back at your starting position
    # additionally, perform an action at each tile using the current position
    # and direction. this action is executed twice, so make sure it is idempotent
    # if you only want the effect of it running once
    def follow_loop(pos, dirn, action):
        init = pos.copy()

        while True:
            # perform the action using the current position and direction
            action(tuple(pos), dirn)

            # get the next position, and perform the action again but using
            # the same direction. this is necessary to handle corner pipes
            pos = get_next_pos(pos, dirn)
            action(tuple(pos), dirn)

            if pos == init:
                break

            # turn to the new direction
            dirn = tile_outputs[dirn][tiles.index(grid[pos[1]][pos[0]])]

    # find the S
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "S":
                pos = [j, i]
                break

    # find which directions the S links up with
    dirns = []
    if tile_outputs[0][tiles.index(grid[pos[1] - 1][pos[0]])] != -1:
        dirns.append(0)
    if tile_outputs[1][tiles.index(grid[pos[1]][pos[0] + 1])] != -1:
        dirns.append(1)
    if tile_outputs[2][tiles.index(grid[pos[1] + 1][pos[0]])] != -1:
        dirns.append(2)
    if tile_outputs[3][tiles.index(grid[pos[1]][pos[0] - 1])] != -1:
        dirns.append(3)

    # sort the directions to make matching easier
    dirns.sort()

    # replace the S with a tile based on which directions it links up with
    match dirns:
        case [0, 1]:
            s_tile = "L"
        case [0, 2]:
            s_tile = "|"
        case [0, 3]:
            s_tile = "J"
        case [1, 2]:
            s_tile = "F"
        case [1, 3]:
            s_tile = "-"
        case [2, 3]:
            s_tile = "7"

    grid[pos[1]][pos[0]] = s_tile

    # the set of all tiles that make up the loop
    loop_tiles = set()
    # walk along the loop, adding each tile to the set
    follow_loop(pos, dirns[0], lambda t, d: loop_tiles.add(t))

    # get the upper left corner tile. this is always an F, so the direction you
    # will be facing to move to the next tile if moving clockwise is east
    pos = sorted(loop_tiles, key=lambda t: (t[-1], t[0]))[0]
    dirn = 1

    # the set of all tiles that are inside, i.e. enclosed by the loop
    inside_tiles = set()

    # when moving clockwise along the loop, the inside of the enclosure will
    # always be to your right. this action adds the tile(s) immediately to the
    # right of a tile on the loop to the set of inside tiles. tile(s) plural
    # when the loop tile is a corner piece, meaning that it is adjacent to two
    # tiles, not one
    def mark_inside(pos, dirn):
        # get the right direction
        inside_dirn = (dirn + 1) % 4
        inside_tile = get_next_pos(pos, inside_dirn)

        # a tile can only be an inside tile if it is not a part of the loop
        if tuple(inside_tile) not in loop_tiles:
            inside_tiles.add(tuple(inside_tile))

    # walk along the loop, adding the tile on the right of the current tile
    # to the set of inside tiles
    follow_loop(list(pos), dirn, mark_inside)

    # the only inside tiles that haven't been counted already are the ones
    # that aren't adjacent to the loop, i.e. the ones that are part of a larger
    # group of inside tiles, or the ones diagonally adjacent to a corner pipe
    # tile. however, all of these will be adjacent to at least
    # one other inside tile that has already been marked. therefore, for every
    # tile that has not been classified yet, we can check if they are next to
    # an inside tile, and if they are, mark them as inside tiles too
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[i]) - 1):
            if (i, j) not in loop_tiles and (i, j) not in inside_tiles:
                for k in range(i - 1, i + 2):
                    for l in range(j - 1, j + 2):
                        if (k, l) in inside_tiles:
                            inside_tiles.add((i, j))

    print(f'{len(inside_tiles)=}')
    with open('solved_nodes.pkl', 'wb') as f:
        pickle.dump(inside_tiles, f)


def get_next_pos(pos, dirn):
    # given a position and direction, return the position resulting from
    # taking one step in that direction
    match dirn:
        case 0:
            pos = [pos[0], pos[1] - 1]
        case 1:
            pos = [pos[0] + 1, pos[1]]
        case 2:
            pos = [pos[0], pos[1] + 1]
        case 3:
            pos = [pos[0] - 1, pos[1]]

    return pos


if __name__ == "__main__":
    main()
