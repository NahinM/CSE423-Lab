from Drawings import *
from funLib import *
import time
import math
def setupCamera():
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    gluPerspective(window.fovY, window.width/window.height, 0.1, 1500) # Think why aspect ration is 1.25?
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix

    # Extract camera position and look-at target
    x, y, z = Position.cam
    lx,ly,lz = Position.lookAt
    # Position the camera and set its orientation
    gluLookAt(x, y, z,  # Camera position
              lx,ly,lz,  # Look-at target
              0, 0, 1)  # Up vector (z-axis)


def showScreen():
    # Clear color and depth buffers
    glClear(int(GL_COLOR_BUFFER_BIT) | int(GL_DEPTH_BUFFER_BIT))
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, 1000, 800)  # Set viewport size

    setupCamera()  # Configure camera perspective
    floor(Game.level)
    player()  # Draw blocky character at player position
    draw_traps()  # Animate and draw traps for the current level
    glutSwapBuffers()

def keyboardListener(key, x, y):
    pass
    
def specialKeyListener(key, x, y):
    x, y, z, r = Position.player
    # Recompute grid from position to avoid drift
    gx = int(x // window.tile_w)
    gy = int((-y) // window.tile_h)

    r_rad = math.radians(r)
    steps = 10

    # Update rotation
    new_r = r
    if key == GLUT_KEY_RIGHT:
        new_r -= 5
    if key == GLUT_KEY_LEFT:
        new_r += 5
    if new_r >= 360:
        new_r -= 360
    if new_r < 0:
        new_r += 360

    # Desired delta
    dx = dy = 0.0
    if key == GLUT_KEY_UP:
        dx = steps * math.sin(r_rad)
        dy = -steps * math.cos(r_rad)
    elif key == GLUT_KEY_DOWN:
        dx = -steps * math.sin(r_rad)
        dy = steps * math.cos(r_rad)

    maze = Mazes.maze[Game.level - 1]
    max_row = len(maze) - 1
    max_col = len(maze[0]) - 1

    def is_wall(mr, mc):
        if mr < 0 or mc < 0 or mr > max_row or mc > max_col:
            return True
        return maze[mr][mc] == '1'

    m_row = gy * 2 + 1
    m_col = gx * 2 + 1

    # Move along X
    new_x = x
    if dx != 0.0:
        try_x = x + dx
        ngx_try = int(try_x // window.tile_w)
        if ngx_try == gx:
            new_x = try_x
        elif ngx_try > gx:
            # moving right -> check right wall
            if not is_wall(m_row, m_col + 1):
                new_x = try_x
                gx = ngx_try
                m_col = gx * 2 + 1
            else:
                # clamp to just before wall
                boundary = (gx + 1) * window.tile_w - 1.0
                new_x = min(try_x, boundary)
        else:  # ngx_try < gx, moving left
            if not is_wall(m_row, m_col - 1):
                new_x = try_x
                gx = ngx_try
                m_col = gx * 2 + 1
            else:
                boundary = gx * window.tile_w + 1.0
                new_x = max(try_x, boundary)

    # Move along Y
    new_y = y
    if dy != 0.0:
        try_y = y + dy
        ngy_try = int((-try_y) // window.tile_h)
        if ngy_try == gy:
            new_y = try_y
        elif ngy_try > gy:
            # moving to next row (downwards) -> check bottom wall
            if not is_wall(m_row + 1, m_col):
                new_y = try_y
                gy = ngy_try
                m_row = gy * 2 + 1
            else:
                boundary = -(gy + 1) * window.tile_h + 1.0
                new_y = max(try_y, boundary)
        else:  # ngy_try < gy, moving to previous row (upwards) -> check top wall
            if not is_wall(m_row - 1, m_col):
                new_y = try_y
                gy = ngy_try
                m_row = gy * 2 + 1
            else:
                boundary = -gy * window.tile_h - 1.0
                new_y = min(try_y, boundary)

    Position.player = [new_x, new_y, z, new_r]
    Position.player_grid = [gx, gy]

def mouseListener(button, state, x, y):
    # On left mouse click, toggle camera state
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        window.cam_state = (window.cam_state + 1) % 2
        cam_state()

def animation():
    time.sleep(1/100)
    cam_state()
    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(int(GLUT_DOUBLE) | int(GLUT_RGB) | int(GLUT_DEPTH))  # Double buffering, RGB color, depth test
    glutInitWindowSize(window.width, window.height)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"Maze Shooter 3D")  # Create the window

    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(animation)  # Register the idle function to move the bullet automatically

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()