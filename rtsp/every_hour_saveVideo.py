import time
import cv2
from multiprocessing import Process
import datetime
import os

# def process():
#     a_list = ["rtsp://xx:xx@xx:xx//Streaming/Channels/2",
#               "rtsp://xx:xx@xx:xx//Streaming/Channels/2",
#               "rtsp://xx:xx@xx:xx//Streaming/Channels/2",
#               "rtsp://xx:xx@xx:xx//Streaming/Channels/2"]
#
#     processes = []
#     for ab in a_list:
#         t = Process(target=video_save, args=(ab,))
#         processes.append(t)
#
#     for i in range(len(a_list)):
#         processes[i].start()
#
#     for j in range(len(a_list)):
#         processes[j].join()


def allday_videos_save():
    print("================")
    print("视频正在截取中")
    print("================")

    cap_url = "rtsp://xx:xx@xx:xx//Streaming/Channels/2"

    cap_port = []
    for j in cap_url:
        if j.isdigit():
            cap_port.append(j)
    cap_port = cap_port[16:-1]
    cap_port = [''.join(cap_port[:5])][0]

    cap = cv2.VideoCapture(cap_url)

    fps = cap.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))  # 摄像头画面的大小
    ret, frame = cap.read()
    target_frame = fps * 60 * 60 * 24 # 24小时的总帧数
    time_frame = fps * 60 * 1  # 设置保存时间为一小时保存一次
    num = 0

    while ret:
        Tim = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        if target_frame - time_frame <= 0:
            break

        else:
            if num == 0:
                video_savename = cap_port + "+" + Tim + ".mp4"
                filename = "H:/video/{}/".format(cap_port + "+" + Tim)
                if not os.path.exists(filename):
                    os.mkdir(filename)
                video_writer = cv2.VideoWriter(filename + video_savename, fourcc, fps, size,True)  # 参数：视频文件名，格式，每秒帧数，宽高，是否灰度
            ret, frame = cap.read()
            # cv2.imshow("frame", frame)
            # img = cv2.resize(frame, (640, 360), interpolation=cv2.INTER_LINEAR)
            video_writer.write(frame)
            num = num + 1
            if num == time_frame:
                video_writer.release()
                num = 0


    # video_writer.release()
    cv2.destroyAllWindows()
    cap.release()

def get_videoName():
    all_videoName = []  # 存放视频名前缀
    video_hour = str(random_time[3])
    video_port = str(url_port)
    select_date = str(random_time[0]) + "-" + str(random_time[1]) + "-" + str(random_time[2])

    for root, dirs, files in os.walk("H:/video/{}/{}".format(video_port,select_date)):
        for file in files:
            all_videoName.append(file.split(".")[0])

    if video_hour in all_videoName:
        videoPath = "H:/video/{}/{}/{}.mp4".format(video_port,select_date,video_hour)

    return videoPath


def deal_videos():
    start = time.time()

    videoPath = get_videoName()

    toDeal_video = cv2.VideoCapture(videoPath)

    total = toDeal_video.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = toDeal_video.get(cv2.CAP_PROP_FPS)
    h = toDeal_video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    w = toDeal_video.get(cv2.CAP_PROP_FRAME_WIDTH)
    print('视频总帧数：{} \t 视频帧速：{} \t 视频大小：{}，{}'.format(total, fps, h, w))

    one_hour_datatime = datetime.datetime(int(random_time[0]), int(random_time[1]), int(random_time[2]),int(random_time[3])+1,0,0)
    # 手动输入的时间
    input_datatime = datetime.datetime(int(random_time[0]), int(random_time[1]), int(random_time[2]),int(random_time[3]), int(random_time[4]), int(random_time[5]))
    needToSave_fps = int((one_hour_datatime - input_datatime).total_seconds()) * fps
    save_video_name = "{}-{}-{}-{}-{}-{}".format(int(random_time[0]), int(random_time[1]), int(random_time[2]),int(random_time[3]), int(random_time[4]), int(random_time[5]))

    size = (int(w), int(h))  # 原视频的大小
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    video_save = str(url_port) + "+" + save_video_name + ".mp4"
    videoWriter = cv2.VideoWriter( "H:/end_save/" + video_save + '.mp4', fourcc, fps, size)

    frameToStart = total - needToSave_fps  # 开始帧
    frametoStop = total  # 结束帧
    toDeal_video.set(cv2.CAP_PROP_POS_FRAMES, frameToStart)  # 设置读取的位置,从第几帧开始读取视频

    count_frame = frameToStart
    while toDeal_video.isOpened():
        success, frame = toDeal_video.read()
        count_frame += 1
        if success:
            if (count_frame >= frameToStart and count_frame <= frametoStop):
                videoWriter.write(frame)
            else:
                break
        else:
            print('截取视频结束')
            break
    end = time.time()
    print("截取视频耗时：", end - start)

if __name__ == '__main__':
    url_port = int(input("请输入端口号："))
    random_time = input("请输入年 月 日 时 分 秒：").split()

    deal_videos()
    #allday_videos_save()
