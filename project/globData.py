class window:
    width = 1200
    height = 800
    cam_state = 0
    fovY = 120
    grid = 600
    wall_heigth = 70
    tile_w = 200
    tile_h=200

class Position:
    player = (0,0,0)
    cam_pos = (0,100,300)
    lookAt = (0,0,0)

class Color:
    floor = [(1,0,1),(1,1,0)]
    wall = (1,0,0)

class Game:
    score = 0
    lives = 5
    level = 1

class Mazes:
    maze = list()

with open("level1.txt") as fl:
            m = list()
            for line in fl:
                m.append([c for c in line if c!='\n'])
            Mazes.maze.append(m)

if __name__=='__main__':
    print(Mazes.maze[0])