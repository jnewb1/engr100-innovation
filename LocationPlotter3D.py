from visual import *
import Utils

scene2 = display(title='Team Ma(i)ze Innovation',
                 x=0, y=0, width=600, height=600,
                 center=(0, 0, 0), autoscale=False, range=1.25, forward=vector(0, 0.5, -1),
                 userzoom=True, background=(1,1,1))

frame = box(pos=(0, 0, 0), length=0.15, height=0.15, width=0.01, color=color.green)
#rotor1 = cylinder(pos=(0.05, 0.05, 0), axis=vector(0.01,0,0), radius=0.02)


quad = frame

floor = box(pos=(-.75, .75, 0), length=2.5, height=2.5, width=0.01, color=color.blue)

class DataSample:
    def __init__(self, point):
        self.dist_forward = point[1][1]
        self.dist_right = point[1][3]
        self.dist_backward = point[1][5]
        self.dist_left = point[1][7]

        self.pitch = point[2][3] * (6.28 / 360)
        self.roll = point[2][1] * (6.28 / 360)
        self.yaw = point[2][5] * (6.28 / 360)

        self.rngfnd = point[3][0]
        self.time_ms = point[0]/10000.0

    
    time_ms = 0
    yaw = 0
    pitch = 0
    roll = 0
    dist_left = 0
    dist_right = 0
    dist_forward = 0
    dist_backward = 0
    rngfnd = 0



wall_width = 0.4
wall_length = 0.4
wall_height = 0.01
# right wall
w1 = box(pos=(0, 0, 0), length=wall_length, height=wall_height, width=wall_width, color=color.red)
w1.rotate(angle=radians(90), axis=vector(0, 0, 1))
# down wall
w2 = box(pos=(0, 0, 0), length=wall_length, height=wall_height, width=wall_width, color=color.red)
# front wall
w3 = box(pos=(0, 0, 0), length=wall_length, height=wall_height, width=wall_width, color=color.red)
# left wall
w4 = box(pos=(0, 0, 0), length=wall_length, height=wall_height, width=wall_width, color=color.red)
w4.rotate(angle=radians(90), axis=vector(0, 0, 1))

def draw_walls(data):
    w1.pos = quad.pos
    w1.pos.x += data.dist_right
    w1.opacity = 1 if data.dist_right < 2 else 0
    w2.pos = quad.pos
    w2.pos.y -= data.dist_backward
    w2.opacity = 1 if data.dist_backward < 2 else 0
    w3.pos = quad.pos
    w3.pos.y += data.dist_forward
    w3.opacity = 1 if data.dist_forward < 2 else 0
    w4.pos = quad.pos
    w4.pos.x -= data.dist_left
    w4.opacity = 1 if data.dist_left < 2 else 0

def fabsmin(a, b):
    if(fabs(a)<fabs(b)):
        return a
    return b

def calculate_movement_vector(last, cur):
    dx = fabsmin(-(last.dist_left - cur.dist_left), last.dist_right - cur.dist_right )
    if(fabs(dx) > 0.1):
        dx = 0
    dy = fabsmin(last.dist_forward - cur.dist_forward, -(last.dist_backward - cur.dist_backward))
    if(fabs(dy) > 0.1):
        dy = 0

    return vector(dx,dy)

def rotate_quad(cur):
    yaw = cur.yaw
    pitch = cur.pitch
    roll = cur.roll
    axis=(cos(pitch)*cos(yaw),-cos(pitch)*sin(yaw),sin(pitch)) 
    up=(sin(roll)*sin(yaw)+cos(roll)*sin(pitch)*cos(yaw),sin(roll)*cos(yaw)-cos(roll)*sin(pitch)*sin(yaw),-cos(roll)*cos(pitch))
    quad.axis = axis
    quad.up = up
    quad.length=.15
    quad.height=.15
    quad.width=0.01
    

def draw_course(data):
    quad.pos = (0, 0, 0)
    data = data[100:]

    last = DataSample(data[0])

    for i, point in enumerate(data):
        cur = DataSample(point)
        dt = cur.time_ms - last.time_ms
        rate(5)

        draw_walls(cur)

        vel = calculate_movement_vector(last, cur)
        quad.x += vel.x
        quad.y += vel.y
        quad.z = cur.rngfnd - .15

        #rotate_quad(cur)

        last = cur

        scene2.center = quad.pos


def run():
    data_file = "C:/Users/justin/source/engr100/innovation/data/108 4-8-2019 1-04-41 PM.data"
    
    data = Utils.load_data(data_file)
    scene2.waitfor('mousedown')
    draw_course(data)


run()

