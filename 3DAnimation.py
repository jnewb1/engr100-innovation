from visual import *

scene2 = display(title='Examples of Tetrahedrons',
                 x=0, y=0, width=600, height=600,
                 center=(0, 0, 0), autoscale=False, range=5, forward=vector(0, 0, -1))

quad = box(pos=(0, 0, 0), length=0.2, height=0.01, width=0.2, color=color.red)

"""
w1 = box(pos=(0,0,0), length=4, height=0.1, width=2, color=color.blue)
w1.rotate(angle=radians(90), axis=vector(0,0,1))
w2 = box(pos=(-3,2,0), length=6, height=0.1, width=2, color=color.red)
w3 = box(pos=(-6,-2,0), length=6, height=0.1, width=2, color=color.red)
w4 = box(pos=(-9,2,0), length=8, height=0.1, width=2, color=color.blue)
w4.rotate(angle=radians(90), axis=vector(0,0,1))
w5 = box(pos=(-6,6,0), length=6, height=0.1, width=2, color=color.red)
w6 = box(pos=(0,5,0), length=6, height=0.1, width=2, color=color.blue)
w6.rotate(angle=radians(90), axis=vector(0,0,1))

"""
# right wall
w1 = box(pos=(0, 0, 0), length=1, height=0.01, width=1, color=color.red)
w1.rotate(angle=radians(90), axis=vector(0, 0, 1))
# down wall
w2 = box(pos=(-3, 2, 0), length=1, height=0.01, width=1, color=color.red)
# front wall
w3 = box(pos=(-6, -2, 0), length=1, height=0.01, width=1, color=color.red)
# left wall
w4 = box(pos=(-9, 2, 0), length=1, height=0.01, width=1, color=color.red)
w4.rotate(angle=radians(90), axis=vector(0, 0, 1))


def draw_walls(pos, up, right, down, left):
    w1.pos = quad.pos
    w1.pos.x += right
    w2.pos = quad.pos
    w2.pos.y -= down
    w3.pos = quad.pos
    w3.pos.y += up
    w4.pos = quad.pos
    w4.pos.x -= left


floor = box(pos=(0, 0, 0), length=5, height=5, width=0.01, color=color.blue)
import re
from ast import literal_eval
import glob

data = []


def load_data():
    global data
    data = []
    with open(data_file, "r") as file:
        for line in file:
            m = re.search(r"\((\d*), \[(.*)\], \[(.*)\], \[(.*)\]\)", line)
            time = m.group(1)
            loc = m.group(2)
            loc = literal_eval(loc)
            att = m.group(3)
            att = literal_eval(att)
            rfnd = m.group(4)
            rfnd = literal_eval(rfnd)
            data.append((int(time), loc, att, rfnd))


def normalize(v):
    norm = np.linalg.norm(v, ord=1)
    if norm == 0:
        norm = np.finfo(v.dtype).eps
    return v / norm


def draw_course():
    global data

    data = data[700:]

    quad.pos = (0, 0, 0)

    last_point = (0, [0, 0, 0, 0, 0, 0, 0, 0])

    for i, point in enumerate(data):
        rate(20)
        using_f = False
        using_r = False
        if (last_point[0] != 0):

            dt = point[0] - last_point[0]
            dt = dt / 10000.0

            lf = last_point[1][1]
            ll = last_point[1][3]
            lb = last_point[1][5]
            lr = last_point[1][7]

            f = point[1][1]
            l = point[1][3]
            b = point[1][5]
            r = point[1][7]

            dx = 0
            dy = 0

            if (f < b):
                if (using_f):
                    dy = -(f - lf)
                using_f = True
            else:
                if (not using_f):
                    dy = (b - lb)
                using_f = False
            if (r < l):
                if (using_r):
                    dx = -(r - lr)
                using_r = True
            else:
                if (not using_r):
                    dx = (l - ll)
                using_r = False

            draw_walls(quad.pos, point[1][1], point[1][3], point[1][5], point[1][7])

            # dx = point[2][1] # x and y derivative using tilt
            # dy = -point[2][3]

            dir = [-dx, -dy]

            # quad.pos.x += dir[0]
            # quad.pos.y += dir[1]

            quad.pos.z = point[3][0]

            pitch = point[2][3] * (6.28 / 360)
            roll = point[2][1] * (6.28 / 360)
            yaw = point[2][5] * (6.28 / 360)

            """
           axis=(-cos(pitch)*cos(yaw),-cos(pitch)*sin(yaw),sin(pitch)) 
            up=(sin(roll)*sin(yaw)+cos(roll)*sin(pitch)*cos(yaw),-sin(roll)*cos(yaw)+cos(roll)*sin(pitch)*sin(yaw),cos(roll)*cos(pitch))
            quad.axis=axis
            quad.up=up
            """

            scene2.center = quad.pos

        last_point = point


def run():
    global data_file
    # for file in glob.glob("C:/Users/justin/Documents/Winter 2018/ENGR100/Innovation/data/*.data"):
    # data_file = file.replace(".data", "")
    data_file = "C:/Users/justin/Documents/Winter 2018/ENGR100/Innovation/data/109 4-8-2019 1-20-31 PM.data"
    load_data()
    draw_course()


run()

