import Utils
import glob

data_file= "data/37 3-22-2019 5-12-24 PM"

def run():
    for file in glob.glob("data/*.data"):
        data_file = file.replace(".data", "")
        data = Utils.load_data(data_file)
        course = Utils.draw_course(data)
        Utils.save_course(course, data_file + ".jpg")



if __name__ == "__main__" :
    run()

course_size = (10, 10)
pix_per_m = 500

start_pt = [5,5]

def course_point(pt):
    return tuple([int(pix_per_m*x) for x in pt])

def course_wall(pt, dir, course):
    if(dir == 0):
        pt1 = (pt[0]-0.1, pt[1])
        pt2 = (pt[0]+0.1, pt[1])
    if(dir == 1):
        pt1 = (pt[0], pt[1]-0.1)
        pt2 = (pt[0], pt[1]+0.1)

    cv2.line(course, course_point(pt1), course_point(pt2), (255,0,0), 1)

def course_quad(pt, course):
    cv2.circle(course, course_point(pt), 5, (0,255,0), -1)

def normalize(v):
    norm=np.linalg.norm(v, ord=1)
    if norm==0:
        norm=np.finfo(v.dtype).eps
    return v/norm

def draw_course():
    global data

    course_pix_size = tuple([pix_per_m*x for x in course_size])
    course = np.zeros((course_pix_size[0], course_pix_size[1], 3), np.uint8)

    cur_pt = start_pt

    last_point = (0, [0,0,0,0,0,0,0,0])

    for point in data:
        if(last_point[0] != 0):

            dt = point[0] - last_point[0]

            #dx_l = ((point[1][3]-last_point[1][3]) + (point[1][7]-last_point[1][7]))/2  # x and y derivative using lidar
            #dy_l = ((point[1][1]-last_point[1][1]) + (point[1][5]-last_point[1][5]))/2

            dx = point[2][1] # x and y derivative using tilt
            dy = point[2][3]

            dir = [dx/100,dy/100]

            cur_pt[0] += dir[0]
            cur_pt[1] += dir[1]

            course_quad(cur_pt, course)

            if point[1][1] != -1 and point[1][1] < 3:
                course_wall((cur_pt[0], cur_pt[1] + point[1][1]), 0, course)  # draw downwards wall

            if point[1][5] != -1 and point[1][5] < 3:
                course_wall((cur_pt[0], cur_pt[1] - point[1][5]), 0, course)  # draw upwards wall

            if point[1][3] != -1 and point[1][3] < 3:
                course_wall((cur_pt[0] - point[1][3], cur_pt[1]), 1, course)  # draw right wall

            if point[1][7] != -1 and point[1][7] < 3:
                course_wall((cur_pt[0] + point[1][7], cur_pt[1]), 1, course)  # draw left wall


        last_point = point

    return course

def save_course(course, filename):
    cv2.imwrite(filename, course)