import cv2
import datetime
import time
from PIL import Image
import pytesseract
import os
from threading import Thread
import logging

'''
format=%(asctime)s具体时间 %(filename)s文件名 
    %(lenvelname)s日志等级 %(message)s具体信息
    datemt=%a星期 %d日期 %b月份 %Y年份 %H:%M:%S时间
'''
logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.DEBUG,
                    filename='cat_deal_video.log',
                    filemode='a')


def target_frame():
    # 截取视频的第一帧
    current_frame = 1
    cameraCapture.set(cv2.CAP_PROP_POS_FRAMES, current_frame)

    while cameraCapture.isOpened():
        success, frame = cameraCapture.read()
        if success:
            video_first_fps = frame
        else:
            break

    # ocr
    gray = cv2.cvtColor(video_first_fps, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]  # 二值化操作

    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)  # 在当前文件中创建新文件，把gray数据写入filename路径中

    # 识别中文，不加lang='chi_sim'默认识别英文
    # image_to_string将图像上的Tesseract OCR运行结果返回到字符
    text = pytesseract.image_to_string(Image.open(filename), lang='chi_sim')
    logging.info(text)
    print(text)

    # 处理识别出来的文字，只保留时间
    data = []
    for j in list(text):
        if j.isdigit():
            data.append(j)
    data = data[:14]
    print(data)
    
    #处理摄像头时间与本地时间不一致
    try:
        if len(data) == 14:
            video_year = [''.join(data[:4])][0]
            video_year1 = [''.join(data[:1])][0]
            data = data[1:]
            if int(video_year) > 2025 and int([''.join(data[:1])][0]) != 0:
                data = data[1:]
                video_year = video_year1 + "0" + [''.join(data[:2])][0]
                data = data[2:]
            else:
                data = data[4:]
        if len(data) == 10:
            video_month = [''.join(data[:2])][0]
            data = data[2:]
        if len(data) == 8:
            video_day = [''.join(data[:2])][0]
            if int(video_day) > 31 and int([''.join(data[:1])][0]) > 3:
                data = data[1:]
                video_day = "0" + [''.join(data[:1])][0]
                data = data[1:]
            else:
                data = data[2:]
        if len(data) == 6:
            video_hour = [''.join(data[:2])][0]
            data = data[2:]
        if len(data) == 4:
            video_minutes = [''.join(data[:2])][0]
            video_seconds = [''.join(data[-2:])][0]
        print(video_year, video_month, video_day, video_hour, video_minutes, video_seconds)
    except:
        logging.error('operation_deal_datatime error!  or  ocr_deal_datatime error!')

    os.remove(filename)  # 删除ocr读取图片，做二值化处理临时存放的文件

    # cv2.imshow("Image", video_first_fps)
    # cv2.imshow("Output", gray)
    cv2.waitKey(0)

    # 截取视频第一帧的时间
    first_fps_datatime = datetime.datetime(int(video_year), int(video_month), int(video_day), int(video_hour), int(video_minutes),int(video_seconds))
    # 手动输入的时间
    input_datatime = datetime.datetime(int(random_time[0]), int(random_time[1]), int(random_time[2]), int(random_time[3]),int(random_time[4]), int(random_time[5]))
    target_fps = int((input_datatime - first_fps_datatime).total_seconds()) * fps
    save_video_name = "{}-{}-{}-{}-{}-{}".format(int(random_time[0]), int(random_time[1]), int(random_time[2]), int(random_time[3]), int(random_time[4]), int(random_time[5]))
    return target_fps, save_video_name


def process():
    processes = []
    for ab in all_list:
        t = Process(target=video, args=(ab,))
        processes.append(t)

    for i in range(len(all_list)):
        processes[i].start()

    for j in range(len(all_list)):
        processes[j].join()

def deal_videos():
    target_fps, save_video_name = target_frame()

    size = (int(w), int(h))  # 原视频的大小
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    videoWriter = cv2.VideoWriter(save_video_name + '.mp4', fourcc, fps, size)

    frameToStart = target_fps - 10*fps # 开始帧 = 输入时间的前五分钟*帧率
    frametoStop = target_fps + 10*fps  # 结束帧 = 输入时间的后五分钟*帧率
    cameraCapture.set(cv2.CAP_PROP_POS_FRAMES, frameToStart)  # 设置读取的位置,从第几帧开始读取视频

    count_frame = frameToStart
    while cameraCapture.isOpened():
        success, frame = cameraCapture.read()
        count_frame += 1
        if success:
            if (count_frame >= frameToStart and count_frame <= frametoStop):
                videoWriter.write(frame)
            else:
                break
        else:
            print('end')
            break
    end = time.time()
    print("截取视频耗时：", end - start)


if __name__ == '__main__':
    start = time.time()
    cameraCapture = cv2.VideoCapture('2022_12_06_15_10_49.mp4')

    total = cameraCapture.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = cameraCapture.get(cv2.CAP_PROP_FPS)
    h = cameraCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    w = cameraCapture.get(cv2.CAP_PROP_FRAME_WIDTH)
    print('视频总帧数：{} \t 视频帧速：{} \t 视频大小：{}，{}'.format(total, fps, h, w))

    random_time = input("请输入年 月 日 时 分 秒：").split()

    deal_videos()
