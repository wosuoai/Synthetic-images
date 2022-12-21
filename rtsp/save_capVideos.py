import time
import cv2
from multiprocessing import Process
from datetime import datetime
import os,yaml


# 返回远程摄像头的小时数
def get_rtsp_time() -> str:
    t = int(time.time())
    h = datetime.fromtimestamp(t).strftime('%H')
    m = datetime.fromtimestamp(t).strftime('%M')
    H = str(int(h) * 60 + int(m))
    return H


def process_caps():

    f = open("1.yaml")
    z = yaml.load(f, Loader=yaml.FullLoader)

    for mer_key in z:
        # 遍历出每个商户
        mer_item = z[mer_key]
        # 遍历出商户里所有摄像头对象
        for cap_key in mer_item:
            # 获取摄像头对象里所有属性
            shopid = mer_item[cap_key]['shopid']
            user = mer_item[cap_key]['user']
            password = mer_item[cap_key]['password']
            ip = mer_item[cap_key]['ip']
            port = mer_item[cap_key]['port']
            rtsp_url = "rtsp://{}:{}@{}:{}//Streaming/Channels/2".format(user, password, ip, port)
            print(user,password,ip,port)
            print(rtsp_url)
            t = Process(target=allday_videos_save, args=(rtsp_url, ip, port, shopid,))
            t.start()

def allday_videos_save(cap_url: str, ip, port, shopid) -> None:

    cap = cv2.VideoCapture(cap_url)
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    # 刚开始创建一次文件夹和为第一段视频命名
    Tim = time.strftime("%Y-%m-%d", time.localtime())  # 日期
    count = get_rtsp_time()  # 分钟数
    video_savename = count + ".mp4"
    filename = "./{}/{}/{}/".format(shopid, ip + "+" + port, Tim)  # ./shopid/ip+port/%Y-%m-%d/

    if not os.path.exists(filename):
        os.makedirs(filename)
    # 创建一个视频对象
    video_writer = cv2.VideoWriter(filename + video_savename, fourcc, fps, size, True)  # 参数：视频文件名，格式，每秒帧数，宽高，是否灰度

    while cap.isOpened():
        new_Tim = time.strftime("%Y-%m-%d", time.localtime())
        if new_Tim != Tim:
            filename = "./{}/{}/{}/".format(shopid, ip + "+" + port, Tim)
            os.makedirs(filename)

        ret, frame = cap.read()
        #print("{}分钟的视频正在截取中！".format(count))
        video_writer.write(frame)
        new_count = get_rtsp_time()
        cv2.waitKey(2)

        if int(new_count) - int(count) >= 1:
            video_writer.release()
            #print("%s 视频保存完成" % video_savename)
            # 重新开始计时
            count = new_count
            video_savename = count + ".mp4"
            video_writer = cv2.VideoWriter(filename + video_savename, fourcc, fps, size, True)
            # print("新的视频文件生成成功")

    video_writer.release()
    cv2.destroyAllWindows()
    # cap.release()

def delete():
    import datetime

    f = open("1.yaml")
    z = yaml.load(f, Loader=yaml.FullLoader)

    for mer_key in z:
        # 遍历出每个商户
        mer_item = z[mer_key]
        # 遍历出商户里所有摄像头对象
        for cap_key in mer_item:
            # 获取摄像头对象里所有属性
            shopid = mer_item[cap_key]['shopid']

    file_list = ['./{}'.format(shopid)]  # 文件夹列表
    today = datetime.datetime.now()
    # 计算偏移量,前3天
    offset = datetime.timedelta(days=-3)
    # 获取想要的日期的时间,即前3天时间
    re_date = (today + offset)
    # 前3天时间转换为时间戳
    re_date_unix = time.mktime(re_date.timetuple())

    try:
        while file_list:
            path = file_list.pop()  # 删除列表最后一个元素，并返回
            for item in os.listdir(path):
                path2 = os.path.join(path, item)  # 组合绝对路径
                if os.path.isfile(path2):  # 判断绝对路径是否为文件
                    # 比较时间戳,文件修改时间小于等于3天前
                    if os.path.getmtime(path2) <= re_date_unix:
                        os.remove(path2)
                else:
                    if not os.listdir(path2):
                        # 若目录为空，则删除，并递归到上一级目录
                        os.removedirs(path2)
                    else:
                        # 为文件夹时,添加到列表中。再次循环
                        file_list.append(path2)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    Process(target=delete, args=()).start()
    process_caps()
