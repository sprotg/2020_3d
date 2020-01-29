import matplotlib.pyplot as plt
from math import sin, cos, pi
from ur_programmer import UR_programmer

def f(t):
    #Lissajouskurve
    #Rotationshastighed
    sx = 3
    sy = 3
    #Faseforskydning
    theta = 0.5 + 3 * sin(2*pi*t/1000)
    #Amplitude
    ax = 140*sin(2.01*2*pi*t/1000)
    ay = 120*sin(2*pi*t/1000 + 1)
    x = ax * sin(sx*t + theta)
    y = ay * sin(sy*t)
    return (x,y)

#Rotationsmatricer til at transforme re punkterne? f.eks.
#som et roterende bord? (James Gandy, gandyworks)
#[cv  -sv][x]   [x cv - y sv]
#[sv  cv ][y] = [x sv - y cv]


def trans(p,t):
    #offset
    off = (-425,-400)
    #Rotation
    omega = 0.02
    p = [((p[0] + off[0]) * cos(t*omega) - (p[1] + off[1]) * sin(t*omega))/1000, ((p[0] + off[0]) * sin(t*omega) + (p[1] + off[1]) * cos(t*omega))/1000]
    #print(p)
    return p

def generate_points():
    l = [trans(f(float(t)/(2*pi)), float(t)) for t in range(0,n)]
    minx = miny = 10000
    maxx = maxy = -10000
    sumx = 0
    sumy = 0
    for p in l:
        sumx += p[0]
        sumy += p[1]
        if p[0] > maxx:
            maxx = p[0]
        if p[0] < minx:
            minx = p[0]
        if p[1] > maxy:
            maxy = p[1]
        if p[1] < miny:
            miny = p[1]
    avgx = sumx / len(l)
    avgy = sumy / len(l)
    scalex = maxx - minx
    scaley = maxy - miny
    print("Tegningens størrelse: {},{}".format(scalex,scaley))
    for p in l:
        p[0] -= avgx
        p[1] -= avgy
        p[0] /= scalex
        p[1] /= scaley
        p[0] *= 0.1
        p[1] *= 0.14
        p[0] += -0.425
        p[1] += -0.400

    return l


cmd = ''

tilstand = 0

robotprog = UR_programmer("10.130.58.13", simulate=True)
robotprog.tegnehojde = 0.062
robotprog.tegne_limits = [-0.525, -0.542, -0.325, -0.265]

while tilstand != -1:
    if tilstand == 0:
        cmd = input("Menu> ")
        if cmd == "q":
            tilstand = -1
        elif cmd == "view":
            n=int(2*pi*50)

            points = generate_points()
            xvals = [points[i][0] for i in range(0,len(points))]
            yvals = [points[i][1] for i in range(0,len(points))]

            OTGblue = (0,141/255,156/255)
            plt.plot(xvals, yvals, color=OTGblue)
            plt.show()
        elif cmd == 'draw':
            #Lav job til robottens
            n=int(2*pi*50)
            points = generate_points()
            for i in range(10):
                print(points[i])
            #Send Job
            robotprog.move_path(points)
        elif cmd == 'params':
            pass
        elif cmd == 'home':
            robotprog.move_home()
