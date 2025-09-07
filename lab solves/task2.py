from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

# _______ Task 1 ________

#global variables
winWidth, winHeigth = 1000,800
speed = 5
dx = 0
speed = 70
rain_drops = []

color = {
    "body": (93/255, 166/255, 137/255),
    "roof":(17/255, 120/255, 113/255),
    "window":(0.5,0.5,0.5),
    "door":(155/255, 173/255, 35/255),
    "ground" : (102/255, 107/255, 0/255),
    "rain":(4/255, 188/255, 224/255),
    "background":(0,0,0,1)
}

class rain:
    def __init__(self):
        self.x = random.randrange(1,winWidth-1)
        self.y = random.randrange(1,winHeigth-5)
    
for _ in range(50):
    rain_drops.append(rain())

def draw_box(x,y,w,h):
    glBegin(GL_QUADS)
    glVertex2d(x,y)
    glVertex2d(x,y+h)
    glVertex2d(x+w,y+h)
    glVertex2d(x+w,y)
    glEnd()

def draw_triangle(x,y,w,h):
    glBegin(GL_TRIANGLES)
    glVertex2d(x,y)
    glVertex2d(x+w,y)
    glVertex2d(x+(w//2),y+h)
    glEnd()

def draw_house():
    global color
    glColor3f(*color["body"])
    draw_box(200,200,400,200) # house body
    glColor3f(*color["roof"])
    draw_triangle(200-10,400,400+20,100) # roof
    glColor3f(*color["window"])
    draw_box(220,300,90,90) # window left
    draw_box(490,300,90,90) # window right
    glColor3f(*color["door"])
    draw_box(360,205,80,120) # door
    
def boundary(x,y,w,h):
    global winWidth
    glColor3f(0,1,0)
    for xi in range(x,winWidth,w):
        draw_triangle(xi,y,w,h)

def drop_rain():
    glLineWidth(2)
    glBegin(GL_LINES)
    glColor3f(*color["rain"])
    for rain in rain_drops:
        glVertex2f(rain.x,rain.y)
        glVertex2f(rain.x-dx*15,rain.y+20)
    glEnd()


def iterate():
    glViewport(0, 0, winWidth, winHeigth)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, winWidth, 0.0, winHeigth, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def display():
    global posX,posY,winWidth,winHeigth,color
    glClearColor(*color["background"])
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    iterate()
    glColor3f(*color["ground"])
    draw_box(0,0,winWidth,winHeigth/2) # ground
    boundary(0,350,50,80)
    draw_house()
    drop_rain()
    glutSwapBuffers()

def animate():
    time.sleep(1/60)
    global rain_drops, dx, speed, winWidth, winHeigth
    glutPostRedisplay()
    for rain in rain_drops:
        rain.y = (rain.y-speed)%winHeigth
        rain.x = (rain.x+speed*dx)%winWidth
        if rain.y>(winHeigth-speed): rain.x = random.randrange(1,winWidth-1)

def spacialKeyListener(key,x,y):
    global dx
    if key == GLUT_KEY_LEFT: dx -=1
    if key == GLUT_KEY_RIGHT: dx +=1
    glutPostRedisplay()

def keyListener(key,x,y):
    global color
    intensity = 0.05
    back_intsity = 0.15
    if key == b'l':
        for obj in ["body","roof","window","door","ground","rain"]:
            r,g,b = color[obj]
            color[obj] = (min(r+intensity,1),min(g+intensity,1),min(b+intensity,1))
        r,g,b,a = color["background"]
        color["background"] = (min(r+back_intsity,1),min(g+back_intsity,1),min(b+back_intsity,1),a)
    if key == b'd':
        for obj in ["body","roof","window","door","ground","rain"]:
            r,g,b = color[obj]
            color[obj] = (max(r-intensity,0),max(g-intensity,0),max(b-intensity,0))
        r,g,b,a = color["background"]
        color["background"] = (max(0,r-back_intsity),max(0,g-back_intsity),max(0,b-back_intsity),a)

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(winWidth, winHeigth) #window size
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice") #window name
glutDisplayFunc(display)
glutIdleFunc(animate)

glutSpecialFunc(spacialKeyListener)
glutKeyboardFunc(keyListener)
glutMainLoop()