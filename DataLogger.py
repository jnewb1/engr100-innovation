import re
import os
import glob


orig_file_loc = r"C:/Users/justin/Documents/Winter 2018/ENGR100/Innovation/original/"
data_file_loc = r"C:/Users/justin/Documents/Winter 2018/ENGR100/Innovation/data/Old/"

prx_data = []  # D0,D45,D90,D135,D180,D225,D270,D315
att_data = []  # DR, R, DP, P, DY, Y, ERP, EY
rfnd_data = [] # rfnd, ...

def load_data(orig_file):
    global prx_data
    prx_data = []
    global att_data
    att_data = []
    with open(orig_file, "r") as file:
        for line in file:
            m = re.search(r"(PRX, )(\d*), (.*)", line)
            if(m):
                time = m.group(2)
                log_line = m.group(3).split(",")
                prx_data.append([int(time), map(float, log_line[0:10])])
            m = re.search(r"(ATT, )(\d*), (.*)", line)
            if(m):
                time = m.group(2)
                log_line = m.group(3).split(",")
                att_data.append((int(time), map(float, log_line[0:10])))
            m = re.search(r"(RFND, )(\d*), (.*)", line)
            if (m):
                time = m.group(2)
                log_line = m.group(3).split(",")
                rfnd_data.append([int(time), map(float, log_line[0:10])])

def save_data(data_file):
    with open(data_file, "w") as file:
        for prx in prx_data:
            log = (prx[0], prx[1], find_closest_att(prx[0])[1], find_closest_rfnd(prx[0])[1])
            file.write(str(log) + "\n")

def find_closest_att(time):
    best_att = [0, ()]
    for att in att_data:
        if(abs(time-att[0]) < abs(time-best_att[0])):
            best_att = att

    return best_att

def find_closest_rfnd(time):
    best_att = [0, ()]
    for att in rfnd_data:
        if(abs(time-att[0]) < abs(time-best_att[0])):
            best_att = att

    return best_att

def run():
    global data_file

    for file in glob.glob(orig_file_loc + "*.bin.log"):
        file = os.path.basename(file)
        orig_file = orig_file_loc + file
        data_file = data_file_loc + file.replace(".bin.log", ".data")
        load_data(orig_file)
        save_data(data_file)


if __name__ == "__main__" :
    run()