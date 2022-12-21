import numpy as np
import cv2 as cv
from multiprocessing import Process
import time
import json
from collections import deque
from threading import Thread


def videoSaveAp(pts_ong,shapes):
    Tim = time.strftime("%Y_%m_%d_%H_%M_%S",time.localtime())
    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    read_video = cv.VideoWriter(Tim + ".mp4", fourcc, 30, (shapes[1],shapes[0]))
    for frame in list(pts_ong):
        read_video.write(frame)
        cv.waitKey(10)
    read_video.release()

def Sequy(text):
    print("=================《{}》=======================".format(str(text)))


minute = 2
second = 10

anomaly_f = True
scope_num = 2
A_fps_minute_scope = minute * 60 * 30
A_fps_second_scope = second * 30
print("{} minute = {}".format(minute,A_fps_minute_scope))


def video(video_info,cl):
    pts = deque(maxlen=A_fps_minute_scope)

    cap = cv.VideoCapture(video_info)
    print("N : ", cap.isOpened())
    s = 0
    count = 0
    while True:
        success, frame = cap.read()

        if not success:
            break
        s += 1
        shapes = frame.shape
        pts.append(frame)
        if s == cl or count >= 1:
            Sequy("触发异常点")
            count += 1
        print("count:", count)

        if A_fps_minute_scope / scope_num == count and count >= 1:
            count = 0
            opone = list(pts)
            Sequy("视频截取")
            start = time.time()
            t = Thread(target=videoSaveAp, args=(opone, shapes))
            t.start()
            t.join()
            end = time.time()
            print("time:", (end - start))

        cv.imshow("img", frame)

        if cv.waitKey(27) in [ord("q"), 27]:
            break

if __name__ == '__main__':
    a_list = [["rtsp://xx:xx@xx:xx//Streaming/Channels/2",300],
              ["rtsp://xx:xx@xx:xx//Streaming/Channels/2",200],
              ["rtsp://xx:xx@xx:xx//Streaming/Channels/2",500],
              ["rtsp://xx:xx@xx:xx//Streaming/Channels/2",100]]

    processes = []
    for ab in a_list:
        t = Process(target=video, args=(ab[0],ab[1],))
        processes.append(t)

    for i in range(len(a_list)):
        processes[i].start()

    for i in range(len(a_list)):
        processes[i].join()

