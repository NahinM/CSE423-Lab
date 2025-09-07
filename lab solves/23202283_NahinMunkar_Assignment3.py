from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time,math,random
from collections import deque

class window:
    width = 1200
    heigth = 800
    camera_pos = (0,580,500,0)
    cemera_state = 0
    grid_len = 700
    cam_v = (0,0)

class Game:
    score = 0
    life = 5
    bullet_miss = 0
    end = False
    cheat_mode = False
    pause = False

fovY = 120  # Field of view
enemie_scale = 0

class Position:
    player = (0,0,0,0)
    enemies = [(random.randint(-window.grid_len+50,window.grid_len-50),random.randint(-window.grid_len+50,window.grid_len-50),0) for i in range(5)]
    bullet = deque()
    

# __All colors__
class color:
    floor = (
        (0,0.5,0),
        (1,1,1)
    )
    walls = (
        (1,0,0),
        (0,1,0),
        (0,0,1),
        (0,1,1)
    )
    enemie = (
        (0,0,0), # head
        (1,0,0), # body
    )
    player = (
        (0,0,0), # head
        (0,0.3,0), # body
        (250/255, 219/255, 97/255), # hands
        (0,0,1), # legs
        (0.3,0.3,0.3), # gun
    )
    bullet = (1,0,0)

def restart():
    Position.player = (0,0,0,0)
    Position.enemies = [(random.randint(-window.grid_len+50,window.grid_len-50),random.randint(-window.grid_len+50,window.grid_len-50),0) for i in range(5)]
    Position.bullet = deque()
    Game.score = 0
    Game.life = 5
    Game.bullet_miss = 0
    Game.end = False

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, window.width, 0, window.heigth)  # left, right, bottom, top

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_bullet(x,y):
    glPushMatrix()

    glColor(*color.bullet)
    glTranslatef(x,y,50)
    glutSolidCube(10)

    glPopMatrix()

def draw_player():
    glPushMatrix()

    x,y,z,r = Position.player
    glColor(*color.player[1])
    glTranslatef(x,y,z)
    glRotate(r,0,0,1)
    if Game.end:
        glRotate(-90,1,0,0)
    glTranslate(0,0,80)
    glutSolidCube(60)
    glTranslatef(-20,0,-80)
    glColor(*color.player[3])
    gluCylinder(gluNewQuadric(), 5, 10, 60, 10, 10)
    glTranslatef(40,0,0)
    gluCylinder(gluNewQuadric(), 5, 10, 60, 10, 10)
    glTranslate(-20,0,110)
    glRotatef(90, 1, 0, 0)
    glColor(*color.player[4])
    gluCylinder(gluNewQuadric(), 10, 5, 80, 10, 10)
    glTranslatef(-20,0,0)
    glColor(*color.player[2])
    gluCylinder(gluNewQuadric(), 10, 5, 80, 10, 10)
    glTranslatef(40,0,0)
    gluCylinder(gluNewQuadric(), 10, 5, 80, 10, 10)
    glColor(*color.player[0])
    glRotatef(90, 1, 0, 0)
    glTranslate(-20,0,-20)
    gluSphere(gluNewQuadric(), 20, 10, 10)

    glPopMatrix()


def draw_enemies(x,y,z):
    global enemie_scale
    glPushMatrix()
    scale = 0.5+abs(math.sin(math.radians(enemie_scale)))/2
    glTranslate(x,y,z)
    glScalef(scale,scale,scale)
    glColor(1,0,0)
    gluSphere(gluNewQuadric(), 80, 10, 10)
    glTranslate(0,0,80)
    glColor(0,0,0)
    gluSphere(gluNewQuadric(), 30, 10, 10)

    glPopMatrix()
    

def draw_Floor():
    grid_len = window.grid_len

    glBegin(GL_QUADS)
    # drawing walls
    wall_heigth = 100
    walls = ( # (x1,y1,x2,y2)
        (1,-1,1,1),
        (1,1,-1,1),
        (-1,-1,-1,1),
        (-1,-1,1,-1),
    )
    for i,(x1,y1,x2,y2) in enumerate(walls):
        glColor3f(*color.walls[i])
        glVertex3f(x1*grid_len, y1*grid_len, 0)
        glVertex3f(x1*grid_len, y1*grid_len, wall_heigth)
        glVertex3f(x2*grid_len, y2*grid_len, wall_heigth)
        glVertex3f(x2*grid_len, y2*grid_len, 0)

    # drawing floor
    sg_w,sg_h = 14, 10
    w,h = grid_len*2/sg_w, grid_len*2/sg_h
    s1,s2 = -grid_len,grid_len
    for x in range(sg_w):
        for y in range(sg_h):
            glColor3f(*color.floor[(x+y)%2])
            glVertex3f(s1 + x*w, s2 - y*h, 0)
            glVertex3f(s1 + x*w + w, s2 - y*h, 0)
            glVertex3f(s1 + x*w + w, s2 - y*h - h, 0)
            glVertex3f(s1 + x*w, s2 - y*h - h, 0)
    glEnd()


def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    wall = window.grid_len-20
    x,y,z,r = Position.player
    step = 10
    # Move forward (W key)
    if key == b'w':
        x= max(min(x+step*math.sin(math.radians(r)),wall),-wall)
        y= min(max(y-step*math.cos(math.radians(r)),-wall),wall)

    # # Move backward (S key)
    if key == b's':
        x= min(max(x-step*math.sin(math.radians(r)),-wall),wall)
        y= max(min(y+step*math.cos(math.radians(r)),wall),-wall)


    # # Rotate gun left (A key)
    if not Game.cheat_mode and key == b'a': r+=5

    # # Rotate gun right (D key)
    if not Game.cheat_mode and key == b'd': r-=5
        
    Position.player = (x,y,z,r%360)

    # # Toggle cheat mode (C key)
    if key == b'c': Game.cheat_mode = not Game.cheat_mode

    # # Toggle cheat vision (V key)
    if Game.cheat_mode and key == b'v':
        state = window.cemera_state
        if window.cam_v==(0,0) or state==0 or state==2: state = 3
        window.cemera_state = 4-state
        
    # # Reset the game if R key is pressed
    if key == b'r': restart()
    if key == b'p': Game.pause = not Game.pause


def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    if window.cemera_state !=0: return

    r = window.grid_len-20
    x, y, z, t = window.camera_pos
    if key == GLUT_KEY_UP: z+=5
    if key == GLUT_KEY_DOWN: z-=5
    if key == GLUT_KEY_LEFT: t += 5
    if key == GLUT_KEY_RIGHT: t -= 5
    
    x = math.sin(math.radians(t))*r
    y = math.cos(math.radians(t))*r
    window.camera_pos = (x, y, z, t%360)


def mouseListener(button, state, x, y):
    """
    Handles mouse inputs for firing bullets (left click) and toggling camera mode (right click).
    """
        # # Left mouse button fires a bullet
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        x,y,z,r = Position.player
        Position.bullet.append((x,y,r))

        # # Right mouse button toggles camera tracking mode
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN: window.cemera_state = (window.cemera_state+1)%3


def setupCamera():
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    gluPerspective(fovY, window.width/window.heigth, 0.1, 1500) # Think why aspect ration is 1.25?
    glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    glLoadIdentity()  # Reset the model-view matrix

    # Extract camera position and look-at target

    if window.cemera_state==0:
        x, y, z, t = window.camera_pos
        # Position the camera and set its orientation
        gluLookAt(x, y, z,  # Camera position
                0, 0, 0,  # Look-at target
                0, 0, 1)  # Up vector (z-axis)
    elif window.cemera_state==1:
        x, y, z, r = Position.player
        x2= x+200*math.sin(math.radians(r))
        y2= y-200*math.cos(math.radians(r))
        window.cam_v = (x2,y2)
        # Position the camera and set its orientation
        gluLookAt(x, y, z+180,  # Camera position
                x2, y2, 0,  # Look-at target
                0, 0, 1)  # Up vector (z-axis)
    elif window.cemera_state==2:
        x, y, z, r = Position.player
        x2= x+200*math.sin(math.radians(r))
        y2= y-200*math.cos(math.radians(r))
        x= x-40*math.sin(math.radians(r))
        y= y+40*math.cos(math.radians(r))
        # Position the camera and set its orientation
        gluLookAt(x, y, z+200,  # Camera position
                x2, y2, 0,  # Look-at target
                0, 0, 1)  # Up vector (z-axis)
    elif window.cemera_state==3:
        x, y, z, r = Position.player
        x2,y2 = window.cam_v
        # Position the camera and set its orientation
        gluLookAt(x, y, z+180,  # Camera position
                x2, y2, 0,  # Look-at target
                0, 0, 1)  # Up vector (z-axis)


def idle():
    time.sleep(1/100)
    """
    Idle function that runs continuously:
    - Triggers screen redraw for real-time updates.
    """
    if Game.end: return
    # if Game.pause: return

    if Game.cheat_mode:
        x,y,z,r = Position.player
        r = (r+3)%360
        Position.player = (x,y,z,r)
        for i in range(5):
            ex,ey,ez = Position.enemies[i]
            dx = abs(x-ex)
            dy = abs(y-ey)
            if dx==0: dx=0.001
            t = math.degrees(math.atan(dy/dx))
            if ex<x and y<=ey: t = 180 - t
            elif ex<x and ey<y: t = 180 + t
            elif x<ex and ey<y: t = -t
            t = (t+90)%360
            # print(r,t,f"{dy}: {y},{ey}",f"{dx}: {x},{ex}")
            if abs(abs(t)-abs(r))<1.5:
                Position.bullet.append((x,y,r))

    global enemie_scale
    enemie_scale = (enemie_scale+1)%360
    for i in range(5):
        x,y,z = Position.enemies[i]
        x0,y0,z0,r = Position.player
        if abs(x-x0)<35 and abs(y-y0)<35:
            Game.life -= 1
            Position.enemies[i] = (random.randint(-window.grid_len+50,window.grid_len-50),random.randint(-window.grid_len+50,window.grid_len-50),0)
            continue
        speed = 0.3
        Position.enemies[i] = (x+speed if(abs(x+1-x0)<abs(x-x0)) else x-speed,y+speed if(abs(y+1-y0)<abs(y-y0)) else y-speed,0)
    
    get_bullet = len(Position.bullet)
    for _ in range(get_bullet):
        x,y,r = Position.bullet.popleft()
        if x<=-window.grid_len or window.grid_len<=x or y<=-window.grid_len or window.grid_len<=y:
            Game.bullet_miss+=1
            continue
        flag = False
        for i in range(5):
            ex,ey,ez = Position.enemies[i]
            if abs(x-ex)<30 and abs(y-ey)<30:
                Position.enemies[i] = (random.randint(-window.grid_len+50,window.grid_len-50),random.randint(-window.grid_len+50,window.grid_len-50),0)
                flag = True
                Game.score+=1
                break
        if flag: continue
        speed = 20
        x2= x+speed*math.sin(math.radians(r))
        y2= y-speed*math.cos(math.radians(r))
        Position.bullet.append((x2,y2,r))

    if Game.life<=0 or Game.bullet_miss>=10:
        Game.end = True
        window.cemera_state = 0
    
    # Ensure the screen updates with the latest changes
    glutPostRedisplay()


def showScreen():
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """
    # Clear color and depth buffers
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset modelview matrix
    glViewport(0, 0, window.width, window.heigth)  # Set viewport size

    setupCamera()  # Configure camera perspective

    # Draw the grid (game floor)
    draw_Floor()
    draw_player()
    if Game.end:
        draw_text(10, 770, f"Game Is Over. Your Score Is: {Game.score}.")
        draw_text(10, 740, "Press 'R' To Restart The Game.")
    else:
        for x,y,z in Position.enemies:
            draw_enemies(x,y,z)
        get_bullets = len(Position.bullet)
        for _ in range(get_bullets):
            x,y,r = Position.bullet.popleft()
            draw_bullet(x,y)
            Position.bullet.append((x,y,r))
        # Display game info text at a fixed screen position
        draw_text(10, 770, f"player Life Remaining: {Game.life}")
        draw_text(10, 740, f"Game Score: {Game.score}")
        draw_text(10, 710, f"Player Bullet Missed: {Game.bullet_miss}")

    # draw_shapes()

    # Swap buffers for smooth rendering (double buffering)
    glutSwapBuffers()


# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(window.width, window.heigth)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"Bullet Frenzy - A 3D Game with Player Movement, Shooting, & Cheat Modes")  # Create the window

    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()
