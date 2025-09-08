class window:
    width = 1200
    height = 800
    cam_state = 0
    fovY = 120
    grid = 600
    wall_heigth = 170
    tile_w = 300
    tile_h=300

class Position:
    player = [100.0, -100.0, 0.0, 0.0] # x, y, z, rotation (list for mutability)
    player_grid = [0, 0] # grid x, y
    cam = [80.0, 0.0, 100.0]
    lookAt = [80.0, -210.0, 100.0]

class Color:
    floor = [(1,0,1),(1,1,0)]
    wall = (1,0,0)

class Game:
    score = 0
    lives = 5
    level = 1

class Mazes:
    maze = list()

# The pattern to draw the mase is as follows:
# 1 -> wall
# 0 -> tile
# 1111111 -> row for only walls
# 1010101 -> row for alternating wall and tile
# 1111111 -> row for only walls
# 1010101 -> row for alternating wall and tile
# 1111111 -> row for only walls
# 1010101 -> row for alternating wall and tile
# 1111111 -> row for only walls
# To change the maze layout, edit the walls to 0s.
# the position of tile and wall is fixed. Only the walls can be removed.
# but if the tile has different number other than 0 it means there is an trap with that id.
# the trap are drawn in Drawings.py with the function draw_<trap_id>

with open("level1.txt") as fl:
    m = list()
    for line in fl:
        m.append([c for c in line if c!='\n'])
    Mazes.maze.append(m)

if __name__=='__main__':
    print(Mazes.maze[0])