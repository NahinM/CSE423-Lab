from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
from datetime import datetime

# global variables
W_width,W_height = 700,800


# _____ MPL ______

def mpl(x1,y1,x2,y2,r,fun=lambda x,y:(x,y)):
    dx = x2-x1
    dy = y2-y1
    
    if (dx>=0 and dy>=0) or r==2:
        if abs(dx)>abs(dy) or r==2:
            d = 2*dy-dx
            x,y = x1,y1
            while x<=x2:
                glVertex2f(*fun(x,y))
                x+=1
                if d>0:
                    d+= 2*dy-2*dx
                    y+=1
                else: d+=2*dy
        else: mpl(y1,x1,y2,x2,2,lambda x,y: (y,x)) # z1->z0->z1: (x,y)->(y,x)->(y,x)
    elif dx<0 and dy>=0:
        if abs(dx)<abs(dy): mpl(y1,-x1,y2,-x2,2,lambda x,y: (-y,x)) # z2->z0->z2: (x,y)->(y,-x)->(-y,x)
        else: mpl(-x1,y1,-x2,y2,2,lambda x,y: (-x,y)) # z3->z0->z3: (x,y)->(-x,y)->(-x,y)
    elif dx<0 and dy<0:
        if abs(dx)>abs(dy): mpl(-x1,-y1,-x2,-y2,2,lambda x,y: (-x,-y)) # z4->z0->z4: (x,y)->(-x,-y)->(-x,-y)
        else: mpl(-y1,-x1,-y2,-x2,2,lambda x,y: (-y,-x)) # z5->z0->z5: (x,y)->(-y,-x)->(-y,-x)
    else:
        if abs(dx)<abs(dy): mpl(-y1,x1,-y2,x2,2,lambda x,y: (y,-x)) # z6->z0->z6: (x,y)->(-y,x)->(y,-x)
        else: mpl(x1,-y1,x2,-y2,2,lambda x,y: (x,-y)) # z7->z0->z7: (x,y)->(x,-y)->(x,-y)

# ______MPL______

# ______components______

pause,play,back,close,diamond,bar = 0,1,2,3,4,5
d_speed = 0
pause_game = False
Score = 0
components_size = (
    (50,50),
    (50,50),
    (50,50),
    (50,50),
    (40,50),
    (200,35)
)

padding = 15
component_position = (
    [(W_width//2)-(components_size[pause][0]//2),W_height-padding],
    [(W_width//2)-(components_size[play][0]//2),W_height-padding],
    [padding,W_height-padding],
    [W_width-components_size[close][0]-padding,W_height-padding],
    [200,W_height-padding],
    [200,components_size[bar][1]+padding]
)

component_active = [
    True, # pause
    False, # play
    True, # back
    True, # close
    True, # diamond
    True  # bar
]

component_color = [
    (1,1,0), # pause
    (0,1,0), # play
    (0,1,1), # back
    (1,0,0), # close
    (1,1,0.5), # diamond
    (1,1,1)  # bar
]
# ______components______


def draw_line(x1,y1,x2,y2):
    glPointSize(3)
    glBegin(GL_POINTS)
    mpl(x1,y1,x2,y2,1)
    glEnd()

def draw_polygon(points):
    for i in range(len(points)-1):
        x1,y1=points[i]
        x2,y2=points[i+1]
        draw_line(x1,y1,x2,y2)
    x1,y1=points[-1]
    x2,y2=points[0]
    draw_line(x1,y1,x2,y2)

def iterate():
    global W_width, W_height
    glViewport(0, 0, W_width, W_height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, W_width, 0.0, W_height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def component_pause(x,y):
    glColor(1,1,1)
    global components_size,pause,component_color
    w,h = components_size[pause]
    # draw_polygon([(x,y),(x+w,y),(x+w,y-h),(x,y-h)])
    glColor(*component_color[pause])
    draw_line(x+(w//3),y,x+(w//3),y-h)
    draw_line(x+(w//3)*2,y,x+(w//3)*2,y-h)

def component_play(x,y):
    glColor(1,1,1)
    global components_size,play,component_color
    w,h = components_size[play]
    # draw_polygon([(x,y),(x+w,y),(x+w,y-h),(x,y-h)])
    glColor(*component_color[play])
    draw_polygon([
        (x+int(w*.1),y),
        (x+int(w*.9),y-(h//2)),
        (x+int(w*.1),y-h)
    ])

def component_diamond(x,y):
    glColor(1,1,1)
    global components_size,diamond,component_color
    w,h = components_size[diamond]
    # draw_polygon([(x,y),(x+w,y),(x+w,y-h),(x,y-h)])
    glColor(*component_color[diamond])
    draw_polygon([
        (x+(w//2),y),
        (x+w,y-(h//2)),
        (x+(w//2),y-h),
        (x,y-(h//2))
    ])

def component_close(x,y):
    glColor(1,1,1)
    global components_size,close,component_color
    w,h = components_size[close]
    # draw_polygon([(x,y),(x+w,y),(x+w,y-h),(x,y-h)])
    glColor(*component_color[close])
    draw_line(x,y,x+w,y-h)
    draw_line(x+w,y,x,y-h)

def component_back(x,y):
    glColor(1,1,1)
    global components_size,back,component_color
    w,h = components_size[back]
    # draw_polygon([(x,y),(x+w,y),(x+w,y-h),(x,y-h)])
    glColor(*component_color[back])
    draw_line(x,y-(h//2),x+w,y-(h//2))
    draw_line(x,y-(h//2),x+(w//2),y)
    draw_line(x,y-(h//2),x+(w//2),y-h)

def component_bar(x,y):
    glColor(1,1,1)
    global components_size,bar,component_color
    w,h = components_size[bar]
    # draw_polygon([(x,y),(x+w,y),(x+w,y-h),(x,y-h)])
    glColor(*component_color[bar])
    draw_polygon([
        (x,y),
        (x+w,y),
        (x+int(w*.9),y-h),
        (x+int(w*.1),y-h)
    ])

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    iterate()
    global W_width,W_height,components_size,component_position,component_active, pause,play,back,close,diamond,bar

    if component_active[back]: component_back(component_position[back][0],component_position[back][1])
    if component_active[play]: component_play(component_position[play][0],component_position[play][1])
    if component_active[pause]: component_pause(component_position[pause][0],component_position[pause][1])
    if component_active[close]: component_close(component_position[close][0],component_position[close][1])

    if component_active[diamond]: component_diamond(component_position[diamond][0],component_position[diamond][1])
    if component_active[bar]: component_bar(component_position[bar][0],component_position[bar][1])
    glutSwapBuffers()

def hasCollided():
    global component_position,components_size,diamond,bar
    flag = component_position[bar][1]>component_position[diamond][1]-components_size[diamond][1]
    flag = component_position[bar][1]-components_size[bar][1]<component_position[diamond][1] and flag
    flag = component_position[bar][0] < component_position[diamond][0]+components_size[diamond][0] and flag
    flag = component_position[bar][0]+components_size[bar][0] > component_position[diamond][0] and flag
    return flag

def start_over():
    print("starting Over!")
    global component_active,component_color,component_position,Score,pause_game,bar,diamond,d_speed
    component_color[bar] = (1,1,1)
    pause_game = False
    Score = 0
    d_speed=0
    component_position[diamond][0],component_position[diamond][1] = 200,W_height-padding
    component_active[diamond] = True

def animate():
    global component_position,components_size,component_active,component_color,diamond,W_height,W_height,padding,d_speed,pause_game,Score
    if not component_active[diamond] or pause_game: return
    speed = 0.5 + d_speed
    component_position[diamond][1] = component_position[diamond][1]-speed
    if hasCollided():
        component_position[diamond][1] = W_height-padding
        component_position[diamond][0] = random.randint(0,W_width-components_size[diamond][0])
        Score+=1
        if Score%3==0: d_speed += 0.05
        print(f"Score: {Score}")
    elif component_position[bar][1]-components_size[bar][1]>component_position[diamond][1]:
        print(f"Game Over! Score: {Score}")
        component_active[diamond] = False
        component_color[bar] = (1,0,0)
    
    glutPostRedisplay()

def init():
    glClearColor(0,0,0,0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104,	1,	1,	1000.0)

# def keyboardListener(key,x,y):
#     glutPostRedisplay()

def specialKeyListener(key, x, y):
    global component_position,bar,W_width,components_size,d_speed,component_active,pause_game
    if not component_active[diamond] or pause_game: return
    speed = 10+d_speed*2
    if key == GLUT_KEY_LEFT: component_position[bar][0] = max(0,component_position[bar][0]-speed)
    elif key == GLUT_KEY_RIGHT: component_position[bar][0] = min(W_width-components_size[bar][0],component_position[bar][0]+speed)
    
    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global component_position,components_size,component_active, pause,play,back,close,diamond,bar,pause_game
    if button==GLUT_LEFT_BUTTON:
        if(state == GLUT_DOWN):
            y = W_height-y
            for component in range(6):
                if component in [diamond,bar]: continue
                px,py = component_position[component]
                w,h = components_size[component]
                if (px <= x <= px+w) and (py-h <= y <= py):
                    # print(component)
                    if component == pause and component_active[component]:
                        print("pause")
                        pause_game=True
                        component_active[pause] = False
                        component_active[play] = True
                        glutPostRedisplay()
                        return
                    if component == play and component_active[component]:
                        print("play")
                        pause_game=False
                        component_active[pause] = True
                        component_active[play] = False
                        glutPostRedisplay()
                        return
                    if component == close:
                        print("Good Bye!")
                        glutLeaveMainLoop()
                    if component==back:
                        start_over()

    glutPostRedisplay()

glutInit()
glutInitWindowSize(W_width,W_height)
glutInitWindowPosition(0,0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"Catch the diamonds")
init()

glutDisplayFunc(display)
glutIdleFunc(animate)
# glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)

glutMainLoop()