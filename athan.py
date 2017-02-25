"""

"""

import os
from datetime import datetime
from time import sleep, strptime
import csv

def get_day(isoformat):
    """
    :param isoformat: str from datetime.now()
    :return: string
    """
    return isoformat[0:10]

def get_clock(isoformat):
    """
    :param isoformat: str from datetime.now()
    :return: timestamp
    """
    return strptime(isoformat[11:16], "%H:%M")

def get_times(path,file_name):
    """
    parse a csv file to obtain dates and times of prayers
    :param path:str
    :param file_name:str
    :return:dict
    """
    with open(os.path.join(path, file_name), 'r') as f:
        read = csv.reader(f, delimiter=';')
        dict_times = {}
        for l in read:
            date, fa, th, asser, mog, isch = l
            dict_times[date] = [fa, th, asser, mog, isch]
    return dict_times

path = '/home/pi/raspi-progs'
f_name = 'gebetskalendar.csv'
time_dict = get_times(path, f_name)
count = 0
while True:
    t = datetime.now().isoformat()
    # print('t = {}'.format(t))
    _day = get_day(t)
    if _day in time_dict.keys():
        running_times = [strptime(tt, "%H:%M") for tt in time_dict[_day]]
        while len(running_times) != 0:
            current_clock = datetime.now().isoformat()
            clock = get_clock(current_clock)
            print(datetime.now().isoformat())
            if running_times[0] < clock:
                running_times.pop(0)
            elif running_times[0] == clock:
                if len(running_times) == 4:
                    print(datetime.now().isoformat())
                    os.system('mpg123 -f 20000 -o s /home/pi/Music/tathan.mp3')
                else:
                    print(datetime.now().isoformat())
                    os.system('mpg123 -f 30000 -o s /home/pi/Music/tathan.mp3')
                # print('clock = {}'.format(clock))
                running_times.pop(0)
            else:
                ss = datetime.now().isoformat()
                # print('sleep at ' + ss[11:19])
                # print('length = {}'.format(len(running_times)))
                sleep(15)
    break

