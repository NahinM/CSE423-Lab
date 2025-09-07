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
    "background":(0,0,0,1)
}

class rain:
    def __init__(self):
        self.x = random.randrange(1,winWidth-1)
        self.y = random.randrange(1,winHeigth-5)
    
for _ in range(40):
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
    glLineWidth(1)
    glBegin(GL_LINES)
    glColor3f(4/255, 188/255, 224/255)
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
        for obj in ["body","roof","window","door","ground"]:
            r,g,b = color[obj]
            color[obj] = (min(r+intensity,1),min(g+intensity,1),min(b+intensity,1))
        r,g,b,a = color["background"]
        color["background"] = (min(r+back_intsity,1),min(g+back_intsity,1),min(b+back_intsity,1),a)
    if key == b'd':
        for obj in ["body","roof","window","door","ground"]:
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



# _______ Task 2 ________

# global variables
# W_width,W_height = 1000,800
# speed = 5
# blink = False
# blink_toggle = 20
# points = []
# frozen = False

# class point:
#     def __init__(self,x,y) -> None:
#         self.x = x
#         self.y = y
#         self.color = (random.uniform(0,1),random.uniform(0,1),random.uniform(0,1))
#         self.dir_x = random.choice([-1,1])
#         self.dir_y = random.choice([-1,1])

# points.append(point(W_width>>1,W_height>>1))

# def draw_points():
#     global points, blink, blink_toggle
#     glPointSize(5)
#     glBegin(GL_POINTS)
#     if blink: blink_toggle = (blink_toggle+1)%40
#     for p in points:
#         r,g,b = p.color
#         if blink and blink_toggle<20: glColor(0.0,0.0,0.0)
#         else: glColor(r,g,b)
#         glVertex2f(p.x,p.y)
#     glEnd()
        

# def iterate():
#     global W_width, W_height
#     glViewport(0, 0, W_width, W_height)
#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     glOrtho(0.0, W_width, 0.0, W_height, 0.0, 1.0)
#     glMatrixMode (GL_MODELVIEW)
#     glLoadIdentity()

# def display():
#     glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
#     iterate()
#     draw_points()
#     glutSwapBuffers()

# def animate():
#     if frozen: return
#     time.sleep(1/60)
#     global speed, points
#     glutPostRedisplay()
#     for p in points:
#         if not (0 < (p.x+speed*p.dir_x+5) <W_width) : p.dir_x = -p.dir_x
#         if not (0 < (p.y+speed*p.dir_y+5) <W_height) : p.dir_y = -p.dir_y
#         p.x += speed*p.dir_x
#         p.y += speed*p.dir_y

# def init():
#     glClearColor(0,0,0,0)
#     glMatrixMode(GL_PROJECTION)
#     glLoadIdentity()
#     gluPerspective(104,	1,	1,	1000.0)

# def keyboardListener(key,x,y):
#     global frozen
#     if key == b' ':
#         frozen = not frozen
#     glutPostRedisplay()
    

# def specialKeyListener(key, x, y):
#     global speed
#     if key==GLUT_KEY_UP:
#         speed += 2
#         print("Speed Increased")
#     if key== GLUT_KEY_DOWN:		#// up arrow key
#         speed = max(speed-2,5)
#         print("Speed Decreased")
#     glutPostRedisplay()


# def mouseListener(button, state, x, y):	#/#/x, y is the x-y of the screen (2D)
#     global points, W_height, blink
#     if button==GLUT_RIGHT_BUTTON:
#         if(state == GLUT_DOWN):
#             points.append(point(x,W_height-y))
#     if button==GLUT_LEFT_BUTTON:
#         if(state == GLUT_DOWN):
#             blink = not blink

#     glutPostRedisplay()

# glutInit()
# glutInitWindowSize(W_width,W_height)
# glutInitWindowPosition(0,0)
# glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
# wind = glutCreateWindow(b"test 1 from glut")
# init()

# glutDisplayFunc(display)
# glutIdleFunc(animate)
# glutKeyboardFunc(keyboardListener)
# glutSpecialFunc(specialKeyListener)
# glutMouseFunc(mouseListener)

# glutMainLoop()