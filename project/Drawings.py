from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from globData import *

def player():
    x,y,z,r = Position.player
    glPushMatrix()
    glTranslatef(x,y,z)
    glutSolidCube(60)
    glTranslatef(-20,0,-80)
    
    glPopMatrix()

def draw_tile(px,py,w,h):
    glBegin(GL_QUADS)
    glVertex3f(px,py,0)
    glVertex3f(px+w,py,0)
    glVertex3f(px+w,py-h,0)
    glVertex3f(px,py-h,0)
    glEnd()

def draw_wall(px,py,w,h,top=0,btm=0,lft=0,rgt=0): # walls -> top bottom left right
    wall_h = window.wall_heigth
    glColor3f(*Color.wall)
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
            draw_wall(px,py,window.tile_w,window.tile_h,top=top,btm=btm,lft=lft,rgt=rgt)