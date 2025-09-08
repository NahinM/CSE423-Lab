class window:
    width = 1200
    height = 800
    cam_state = 0
    fovY = 100
    grid = 600
    wall_heigth = 170
    tile_w = 300
    tile_h=300

class Position:
    player = [100.0, -100.0, 0.0, 0.0] # x, y, z, rotation (list for mutability)
    player_grid = [0, 0] # grid x, y
    cam = [80.0, 0.0, 100.0]
    lookAt = [80.0, -210.0, 100.0]

class traps:
    trap_list = list() # each element is [id, px, py] id and position of the trap

class Color:
    floor = [(1,0,1),(1,1,0)]
    wall = [(5/255, 105/255, 3/255),(3/255, 103/255, 105/255)]

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
# there are 3 traps for now with id 2,3,4
# 2 -> spike trap
# 3 -> fire trap
# 4 -> saw trap

with open("level1.txt") as fl:
    m = list()
    for line in fl:
        m.append([c for c in line if c!='\n'])
        for c in line:
            if c not in ['0','1','\n'] and c.isdigit():
                traps.trap_list.append([int(c), len(m)*2-1, (len(m[0])-1)//2*2])
    Mazes.maze.append(m)

if __name__=='__main__':
    print(Mazes.maze[0])