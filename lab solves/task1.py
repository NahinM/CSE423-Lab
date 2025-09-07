from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

# global variables
W_width,W_height = 1000,800
speed = 5
blink = False
blink_toggle = 20
points = []
frozen = False

class point:
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.color = (random.uniform(0,1),random.uniform(0,1),random.uniform(0,1))
        self.dir_x = random.choice([-1,1])
        self.dir_y = random.choice([-1,1])

points.append(point(W_width>>1,W_height>>1))

def draw_points():
    global points, blink, blink_toggle
    glPointSize(5)
    glBegin(GL_POINTS)
    if blink: blink_toggle = (blink_toggle+1)%40
    for p in points:
        r,g,b = p.color
        if blink and blink_toggle<20: glColor(0.0,0.0,0.0)
        else: glColor(r,g,b)
        glVertex2f(p.x,p.y)
    glEnd()
        

def iterate():
    global W_width, W_height
    glViewport(0, 0, W_width, W_height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, W_width, 0.0, W_height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    iterate()
    draw_points()
    glutSwapBuffers()

def animate():
    if frozen: return
    time.sleep(1/60)
    global speed, points
    glutPostRedisplay()
    for p in points:
        if not (0 < (p.x+speed*p.dir_x+5) <W_width) : p.dir_x = -p.dir_x
        if not (0 < (p.y+speed*p.dir_y+5) <W_height) : p.dir_y = -p.dir_y
        p.x += speed*p.dir_x
        p.y += speed*p.dir_y

def init():
    glClearColor(0,0,0,0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104,	1,	1,	1000.0)

def keyboardListener(key,x,y):
    global frozen
    if key == b' ':
        frozen = not frozen
    glutPostRedisplay()
    

def specialKeyListener(key, x, y):
    global speed
    if key==GLUT_KEY_UP:
        speed += 2
        print("Speed Increased")
    if key== GLUT_KEY_DOWN:		#// up arrow key
        speed = max(speed-2,5)
        print("Speed Decreased")
    glutPostRedisplay()


def mouseListener(button, state, x, y):	#/#/x, y is the x-y of the screen (2D)
    global points, W_height, blink
    if button==GLUT_RIGHT_BUTTON:
        if(state == GLUT_DOWN):
            points.append(point(x,W_height-y))
    if button==GLUT_LEFT_BUTTON:
        if(state == GLUT_DOWN):
            blink = not blink

    glutPostRedisplay()

glutInit()
glutInitWindowSize(W_width,W_height)
glutInitWindowPosition(0,0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"test 1 from glut")
init()

glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)

glutMainLoop()