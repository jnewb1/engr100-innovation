from visual import *
import Utils
import copy

scene2 = display(title='Team Ma(i)ze Innovation',
                 x=0, y=0, width=600, height=600,
                 center=(0, 0, 0), autoscale=False, range=1.25, forward=vector(0, 0.5, -0.5),
                 userzoom=True, background=(1,1,1))
frame = frame(pos=(0,0,0))

base1 = box(frame=frame, length=.10, height=.02, width=0.01, pos=(0, 0, 0),color=color.green)
base2 = box(frame=frame, length=.02, height=.10, width=0.01, pos=(0, 0, 0),color=color.green)
r1 = cylinder(frame=frame, pos=(0,.05,0), color=color.cyan, radius=0.02, length=0.02, axis=(0,0,1))
r2 = cylinder(frame=frame, pos=(-.05,0,0), color=color.cyan, radius=0.02, length=0.02, axis=(0,0,1))
r3 = cylinder(frame=frame, pos=(0,-.05,0), color=color.cyan, radius=0.02, length=0.02, axis=(0,0,1))
r4 = cylinder(frame=frame, pos=(.05,0,0), color=color.cyan, radius=0.02, length=0.02, axis=(0,0,1))

quad = frame
quad.rotate(angle=pi/4, axis=(0,0,1), origin=quad.pos)


floor = box(pos=(-1, 1, 0), length=3, height=3, width=0.01, color=color.blue, opacity=0.5)

# Represents one data sample from the quadcopter
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
wall_height = 0.03
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


# draws the four walls in each direction of the quadcopter. If the wall is further than 2 meters, it is not displayed.
def draw_walls(data):
    max_dist = 1.5
    w1.pos = quad.pos
    w1.pos.x += data.dist_right
    w1.opacity = 1 if data.dist_right < max_dist else 0
    w2.pos = quad.pos
    w2.pos.y -= data.dist_backward
    w2.opacity = 1 if data.dist_backward < max_dist else 0
    w3.pos = quad.pos
    w3.pos.y += data.dist_forward
    w3.opacity = 1 if data.dist_forward < max_dist else 0
    w4.pos = quad.pos
    w4.pos.x -= data.dist_left
    w4.opacity = 1 if data.dist_left < max_dist else 0    

def fabsmin(a, b):
    if(fabs(a)<fabs(b)):
        return a
    return b

# calculates how much the quadcopter has moved given two consecutive points
def calculate_movement_vector(last, cur):
    dx = 0
    dy = 0

    min_range = 3

    dxl = -(last.dist_left - cur.dist_left)  # dx using left wall
    dxr = (last.dist_right - cur.dist_right) # dx using right wall

    dyf = (last.dist_forward - cur.dist_forward) # dy using front wall
    dyb = -(last.dist_backward - cur.dist_backward) # dy using back wall

    # Filtering
    if(cur.dist_left < min_range and cur.dist_right < min_range):
        dx = fabsmin(dxl, dxr)
    elif(cur.dist_left < min_range):
        dx = dxl
    elif(cur.dist_right < min_range):
        dx = dxr

    if(cur.dist_forward < min_range and cur.dist_backward < min_range):
        dy = fabsmin(dyf, dyb)
    elif(cur.dist_forward < min_range):
        dy = dyf
    elif(cur.dist_backward < min_range):
        dy = dyb
    
    # High Frequency Filtering
    """
    if(fabs(dx) > 0.3):
        dx = 0
    if(fabs(dy) > 0.3):
        dy = 0
    """
    
    return vector(dx,dy)

# how many data samples to interpolate between each real sample
interpolate_count = 50

# interpolate between two data samples
def interpolate(last, cur, j):
    j = float(j)
    ret = copy.deepcopy(last)
    
    ret.dist_left = last.dist_left + (cur.dist_left - last.dist_left)*(j/interpolate_count)
    ret.dist_right = last.dist_right + (cur.dist_right - last.dist_right)*(j/interpolate_count)
    ret.dist_forward = last.dist_forward + (cur.dist_forward - last.dist_forward)*(j/interpolate_count)
    ret.dist_backward = last.dist_backward + (cur.dist_backward - last.dist_backward)*(j/interpolate_count)
    ret.rngfnd = last.rngfnd + (cur.rngfnd - last.rngfnd)*(j/interpolate_count)
    
    return ret

# draws the course given a set of data samples
def draw_course(data):
    quad.pos = (0, 0, 0) # quadcopter starts at (0,0,0)
    data = data[150:390] # used to filter out the data that is important

    last = DataSample(data[0])

    m_c = 0

    # for each data point, draw the walls, and move the quadcopter
    for i, point in enumerate(data):
        cur = DataSample(point)
        dt = cur.time_ms - last.time_ms
        if(dt == 0):
            dt = 0.00001
        last_i = last
        for j in range(interpolate_count):
            rate(1/(dt/100) * interpolate_count)
            cur_i = interpolate(last, cur, j)
            draw_walls(cur_i)
            vel = calculate_movement_vector(last_i, cur_i)
            quad.x += vel.x
            quad.y += vel.y
            quad.z = cur.rngfnd - .2 # 0.2 is when the quadcopter is on the ground, so subtract this from the reading.
            scene2.center = quad.pos


            last_i = cur_i
        m_c += 1
        if(m_c > 5):
            quad_marker = box(length=.05, height=.05, width=0.01, color = color.red, opacity=0.5)
            quad_marker.pos = quad.pos
            m_c = 0

        #scene2.forward = -vector(cos(i/20.0)*.5,sin(i/20.0)*.5,.5)
        #scene2.up = vector(0,0,1)
        
        
        last = cur



def run():
    data_file = "C:/Users/justin/source/engr100/innovation/data/108 4-8-2019 1-04-41 PM.data"
    
    data = Utils.load_data(data_file)
    while True:
        scene2.waitfor('mousedown')
        draw_course(data)


run()

