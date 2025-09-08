from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from globData import *
import math
import time

def _draw_box(cx, cy, cz, w, d, h, color):
    glPushMatrix()
    glTranslatef(cx, cy, cz)
    glScalef(w, d, h)
    glColor3f(*color)
    glutSolidCube(1.0)
    glPopMatrix()

def player():
    x, y, z, r = Position.player
    glPushMatrix()
    # Position and face direction (rotate around Z axis)
    glTranslatef(x, y, z)
    glRotatef(r, 0, 0, 1)

    # Dimensions (units)
    torso_w, torso_d, torso_h = 40, 20, 60
    head_w, head_d, head_h = 30, 20, 30
    arm_w, arm_d, arm_h = 12, 12, 40
    leg_w, leg_d, leg_h = 15, 15, 40

    # Colors
    body_col = (0.2, 0.6, 0.9)
    limb_col = (0.9, 0.8, 0.7)

    # Torso centered at z = torso_h/2
    _draw_box(0, 0, torso_h * 0.5, torso_w, torso_d, torso_h, body_col)

    # Head on top of torso
    head_z = torso_h + head_h * 0.5
    _draw_box(0, 0, head_z, head_w, head_d, head_h, limb_col)

    # Arms at sides, centered at torso mid-height
    arm_z = torso_h * 0.5
    arm_x_off = torso_w * 0.5 + arm_w * 0.5
    _draw_box(-arm_x_off, 0, arm_z, arm_w, arm_d, arm_h, limb_col)  # Left arm
    _draw_box( arm_x_off, 0, arm_z, arm_w, arm_d, arm_h, limb_col)  # Right arm

    # Legs from ground up
    leg_z = leg_h * 0.5
    leg_x_off = 10
    _draw_box(-leg_x_off, 0, leg_z, leg_w, leg_d, leg_h, limb_col)  # Left leg
    _draw_box( leg_x_off, 0, leg_z, leg_w, leg_d, leg_h, limb_col)  # Right leg

    glPopMatrix()

def draw_tile(px,py,w,h):
    glBegin(GL_QUADS)
    glVertex3f(px,py,0)
    glVertex3f(px+w,py,0)
    glVertex3f(px+w,py-h,0)
    glVertex3f(px,py-h,0)
    glEnd()

def draw_wall(px,py,w,h,top=0,btm=0,lft=0,rgt=0,clr=0): # walls -> top bottom left right
    wall_h = window.wall_heigth
    glColor3f(*Color.wall[clr])
    if top:
        glBegin(GL_QUADS)
        glVertex3f(px,py,0)
        glVertex3f(px+w,py,0)
        glVertex3f(px+w,py,wall_h)
        glVertex3f(px,py,wall_h)
        glEnd()
    if btm:
        glBegin(GL_QUADS)
        glVertex3f(px,py-h,0)
        glVertex3f(px+w,py-h,0)
        glVertex3f(px+w,py-h,wall_h)
        glVertex3f(px,py-h,wall_h)
        glEnd()
    if lft:
        glBegin(GL_QUADS)
        glVertex3f(px,py,0)
        glVertex3f(px,py-h,0)
        glVertex3f(px,py-h,wall_h)
        glVertex3f(px,py,wall_h)
        glEnd()
    if rgt:
        glBegin(GL_QUADS)
        glVertex3f(px+w,py,0)
        glVertex3f(px+w,py-h,0)
        glVertex3f(px+w,py-h,wall_h)
        glVertex3f(px+w,py,wall_h)
        glEnd()

def floor(level=1):
    maze = Mazes.maze[level-1]
    nw,nh = (len(maze[0])-1)>>1,(len(maze)-1)>>1 #number of segments for the floor
    startx,starty = 0,0 #co-ordinates of the floor
    for i in range(nh):
        for j in range(nw):
            glColor3f(*Color.floor[(i+j)%2])
            px,py = startx+j*window.tile_w, starty-i*window.tile_h
            draw_tile(px,py,window.tile_w,window.tile_h)
            
    for i in range(nh):
        m_y = i*2+1
        for j in range(nw):
            m_x = j*2+1
            top=btm=lft=rgt=0
            if maze[m_y-1][m_x]=='1': top=1
            if maze[m_y+1][m_x]=='1': btm=1
            if maze[m_y][m_x-1]=='1': lft=1
            if maze[m_y][m_x+1]=='1': rgt=1
            px,py = startx+j*window.tile_w,starty-i*window.tile_h
            draw_wall(px,py,window.tile_w,window.tile_h,top=top,btm=btm,lft=lft,rgt=rgt,clr=(i+j)%2)

def draw_traps(level=1):
    maze = Mazes.maze[level-1]
    nw,nh = (len(maze[0])-1)>>1,(len(maze)-1)>>1
    startx,starty = 0,0
    # Time parameter for animation
    t = glutGet(GLUT_ELAPSED_TIME) / 1000.0
    for i in range(nh):
        m_y = i*2+1
        for j in range(nw):
            m_x = j*2+1
            c = maze[m_y][m_x]
            if c in ['2','3','4']:
                # Center of the tile
                cx = startx + j*window.tile_w + window.tile_w*0.5
                cy = starty - i*window.tile_h - window.tile_h*0.5
                if c == '2':
                    # spikes: sinusoidal up/down
                    z_shift = 10 + 60 * (0.5 + 0.5 * math.sin(2*math.pi*1.2*t))
                    draw_trap_2(cx, cy, z_shift)
                elif c == '3':
                    # fire: faster flicker up/down
                    z_shift = 20 + 30 * (0.5 + 0.5 * math.sin(2*math.pi*2.5*t + (i+j)))
                    draw_trap_3(cx, cy, z_shift)
                elif c == '4':
                    # saw: gentle bob
                    z_shift = 15 + 25 * (0.5 + 0.5 * math.sin(2*math.pi*0.8*t + j))
                    draw_trap_4(cx, cy, z_shift)

def draw_trap_2(px,py,z_shift):
    # three spikes (Cylinder with sharp end) in a tile
    spike_h = 50
    spike_r = 10
    gap = (window.tile_w - 3*spike_r*2)//4

    for i in range(3):
        x_offset = -spike_r - gap + i * (2 * spike_r + gap)
        glPushMatrix()
        glTranslatef(px + x_offset, py, z_shift)
        gluCylinder(gluNewQuadric(), spike_r, 0, spike_h, 10, 1)
        glPopMatrix()

def draw_trap_3(px,py,z_shift):
    # fire trap: a cone (flame) on a cylinder (base)
    base_h = 20
    base_r = 20
    flame_h = 60
    flame_r = 15

    glPushMatrix()
    glTranslatef(px, py, z_shift)
    glColor3f(0.5, 0.35, 0.05)  # Brown color for base
    gluCylinder(gluNewQuadric(), base_r, base_r, base_h, 10, 1)
    glTranslatef(0, 0, base_h)
    glColor3f(1, 0.5, 0)  # Orange color for flame
    gluCylinder(gluNewQuadric(), flame_r, 0, flame_h, 10, 1)
    glPopMatrix()

def draw_trap_4(px,py,z_shift):
    # saw trap: a thin cylinder (saw blade) on a small cylinder (base)
    base_h = 10
    base_r = 15
    saw_h = 5
    saw_r = 25

    glPushMatrix()
    glTranslatef(px, py, z_shift)
    glColor3f(0.5, 0.35, 0.05)  # Brown color for base
    gluCylinder(gluNewQuadric(), base_r, base_r, base_h, 10, 1)
    glTranslatef(0, 0, base_h)
    glColor3f(0.75, 0.75, 0.75)  # Grey color for saw blade
    gluCylinder(gluNewQuadric(), saw_r, saw_r, saw_h, 30, 1)
    glPopMatrix()