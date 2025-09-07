import sys
sys.stdin = open("input.txt","r")

def zone0_0(x,y):
    return (x,y)

def zone0_1(x,y):
    return (y,x)

def zone0_2(x,y):
    return (-y,x)

def zone0_3(x,y):
    return (-x,y)

def zone0_4(x,y):
    return (-x,-y)

def zone0_5(x,y):
    return (-y,-x)

def zone0_6(x,y):
    return (y,-x)

def zone0_7(x,y):
    return (x,-y)

def zone1_0(x,y):
    return (y,x)

def zone2_0(x,y):
    return (y,-x)

def zone3_0(x,y):
    return (-x,y)

def zone4_0(x,y):
    return (-x,-y)

def zone5_0(x,y):
    return (-y,-x)

def zone6_0(x,y):
    return (-y,x)

def zone7_0(x,y):
    return (x,-y)

def mpl_draw(x1,y1,x2,y2,fun):
    dx = x2-x1
    dy = y2-y1
    
    d = 2*dy-dx
    x,y = x1,y1
    while x!=x2:
        print(*fun(x,y))
        x+=1
        if d>0:
            d+= 2*dy-2*dx
            y+=1
        else: d+=2*dy
    print(*fun(x,y))



def mpl(x1,y1,x2,y2):
    dx = x2-x1
    dy = y2-y1
    
    if dx>=0 and dy>=0:
        if abs(dx)>abs(dy):
            print("z0")
            mpl_draw(x1,y1,x2,y2,lambda x,y: (x,y))
        else:
            # z1->z0->z1: (x,y)->(y,x)->(y,x)
            print("z1") 
            mpl_draw(y1,x1,y2,x2,lambda x,y: (y,x)) 
    elif dx<0 and dy>=0:
        if abs(dx)<abs(dy):
            # z2->z0->z2: (x,y)->(y,-x)->(-y,x)
            print("z2")
            mpl_draw(y1,-x1,y2,-x2,lambda x,y: (-y,x))
        else:
            # z3->z0->z3: (x,y)->(-x,y)->(-x,y)
            print("z3")
            mpl_draw(-x1,y1,-x2,y2,lambda x,y: (-x,y))
    elif dx<0 and dy<0:
        if abs(dx)>abs(dy):
            # z4->z0->z4: (x,y)->(-x,-y)->(-x,-y)
            print("z4")
            mpl_draw(-x1,-y1,-x2,-y2,lambda x,y: (-x,-y))
        else:
            # z5->z0->z5: (x,y)->(-y,-x)->(-y,-x)
            print("z5")
            mpl_draw(-y1,-x1,-y2,-x2,lambda x,y: (-y,-x))
    else:
        if abs(dx)<abs(dy):
            # z6->z0->z6: (x,y)->(-y,x)->(y,-x)
            print("z6")
            mpl_draw(-y1,x1,-y2,x2,lambda x,y: (y,-x))
        else:
            # z7->z0->z7: (x,y)->(x,-y)->(x,-y)
            print("z7")
            mpl_draw(x1,-y1,x2,-y2,lambda x,y: (x,-y)) 

t = 1
t = int(input())
while t>0:
    t-=1
    x1,y1,x2,y2 = list(map(int,input().split()))
    mpl(x1,y1,x2,y2)
    print("---nest---")