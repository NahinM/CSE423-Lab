from Drawings import *
from funLib import *
import time
import math
import random
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
    player()              # Draw blocky character at player position
    draw_traps()          # Animate and draw traps for the current level
    draw_enemies()        # Draw enemies
    draw_bullets()        # Draw bullets
    draw_walls(Game.level)  # Draw walls around the maze
    draw_hud()             # Draw on-screen HUD (score, lives)
    glutSwapBuffers()

def keyboardListener(key, x, y):
    # R: reset score/lives (optional helper)
    if key in (b'R', b'r'):
        Game.score = 0
        Game.lives = 5
    
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
        return maze[mr][mc] in ('#','1')

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
    # Left click: shoot in the view direction
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        px, py, pz, r = Position.player
        s = 20.0
        dx = math.sin(math.radians(r)) * s
        dy = -math.cos(math.radians(r)) * s
        Bullets.items.append({'x': px, 'y': py, 'dx': dx, 'dy': dy, 'speed': s, 'life': 2.5, 'r': r})
    # Right click: toggle camera state
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        window.cam_state = (window.cam_state + 1) % 2
        cam_state()

def animation():
    # time step
    t_now = glutGet(GLUT_ELAPSED_TIME) / 1000.0
    if Game.last_update_time == 0.0:
        Game.last_update_time = t_now
    dt = max(0.0, min(0.05, t_now - Game.last_update_time))
    Game.last_update_time = t_now

    # Camera state
    cam_state()

    # Spawn enemies occasionally (limit alive to 5)
    alive_count = sum(1 for e in Enemies.items if e.get('alive', True))
    if alive_count < 5 and random.random() < 0.02:
        # pick a random open tile
        maze = Mazes.maze[Game.level - 1]
        nh = (len(maze) - 1) // 2
        nw = (len(maze[0]) - 1) // 2
        tries = 0
        while tries < 20:
            gi = random.randint(0, nh - 1)
            gj = random.randint(0, nw - 1)
            m_y = gi * 2 + 1
            m_x = gj * 2 + 1
            if maze[m_y][m_x] == '0':
                ex = gj * window.tile_w + window.tile_w * 0.5
                ey = -gi * window.tile_h - window.tile_h * 0.5
                ang = random.random() * 2 * math.pi
                speed = 150.0  # units per second
                vx = speed * math.cos(ang)
                vy = speed * math.sin(ang)
                Enemies.items.append({'x': ex, 'y': ey, 'alive': True, 'r': 0.0, 'vx': vx, 'vy': vy})
                break
            tries += 1

    # Move enemies (ignore walls, but keep within world bounds)
    maze = Mazes.maze[Game.level - 1]
    nh = (len(maze) - 1) // 2
    nw = (len(maze[0]) - 1) // 2
    min_x, max_x = 0.0, nw * window.tile_w
    min_y, max_y = -nh * window.tile_h, 0.0
    pad = 10.0
    for e in Enemies.items:
        if not e.get('alive', True):
            continue
        vx = e.get('vx', 120.0)
        vy = e.get('vy', 0.0)
        ex = e['x'] + vx * dt
        ey = e['y'] + vy * dt
        bounced = False
        if ex < min_x + pad:
            ex = min_x + pad
            vx = abs(vx)
            bounced = True
        elif ex > max_x - pad:
            ex = max_x - pad
            vx = -abs(vx)
            bounced = True
        if ey < min_y + pad:
            ey = min_y + pad
            vy = abs(vy)
            bounced = True
        elif ey > max_y - pad:
            ey = max_y - pad
            vy = -abs(vy)
            bounced = True
        # slight random drift on bounce to avoid sync
        if bounced:
            ang_jitter = (random.random() - 0.5) * 0.3
            spd = (vx*vx + vy*vy) ** 0.5
            ang = math.atan2(vy, vx) + ang_jitter
            vx = spd * math.cos(ang)
            vy = spd * math.sin(ang)
        e['x'], e['y'], e['vx'], e['vy'] = ex, ey, vx, vy

    # Enemy contact damage to player (cooldown 1s)
    px, py, pz, pr = Position.player
    for e in Enemies.items:
        if not e.get('alive', True):
            continue
        dxp = e['x'] - px
        dyp = e['y'] - py
        if dxp*dxp + dyp*dyp <= (30*30):
            if t_now - Game.last_enemy_hit_time > 1.0:
                Game.lives = max(0, Game.lives - 1)
                Game.last_enemy_hit_time = t_now

    # Update bullets
    for b in list(Bullets.items):
        b['x'] += b['dx']
        b['y'] += b['dy']
        b['life'] -= dt
        # remove old bullets
        if b['life'] <= 0:
            Bullets.items.remove(b)
            continue
        # stop at walls: if crossing a wall edge, remove bullet
        gx = int(b['x'] // window.tile_w)
        gy = int((-b['y']) // window.tile_h)
        m_row = gy * 2 + 1
        m_col = gx * 2 + 1
        maze = Mazes.maze[Game.level - 1]
        # simple bounds check
        if m_row < 1 or m_col < 1 or m_row >= len(maze) - 1 or m_col >= len(maze[0]) - 1:
            Bullets.items.remove(b)
            continue
        # if this is not a floor, remove
        if maze[m_row][m_col] not in ('0', '2', '3', '4'):
            Bullets.items.remove(b)
            continue
        # hit enemy check (circle distance)
        hit_enemy = None
        for e in Enemies.items:
            if not e.get('alive', True):
                continue
            dx = e['x'] - b['x']
            dy = e['y'] - b['y']
            if dx*dx + dy*dy <= (20*20):
                hit_enemy = e
                break
        if hit_enemy is not None:
            hit_enemy['alive'] = False
            Game.score += 5
            if b in Bullets.items:
                Bullets.items.remove(b)

    # Trap damage if player on trap tile (with debounce)
    px, py, pz, pr = Position.player
    gx = int(px // window.tile_w)
    gy = int((-py) // window.tile_h)
    m_row = gy * 2 + 1
    m_col = gx * 2 + 1
    maze = Mazes.maze[Game.level - 1]
    if 0 <= m_row < len(maze) and 0 <= m_col < len(maze[0]):
        if maze[m_row][m_col] in ('2', '3', '4'):
            if t_now - Game.last_trap_hit_time > 1.0:  # 1s cooldown
                Game.lives = max(0, Game.lives - 1)
                Game.last_trap_hit_time = t_now

    # Update window title with score/lives
    try:
        glutSetWindowTitle(f"Maze Shooter 3D | Score: {Game.score}  Lives: {Game.lives}".encode())
    except Exception:
        pass

    time.sleep(1/100)
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