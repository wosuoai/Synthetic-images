import cv2
import numpy
import time
from PIL import Image
import os
import random

import logging

'''format=%(asctime)s具体时间 %(filename)s文件名 %(lenvelname)s日志等级 %(message)s具体信息
   datemt=%a星期 %d日期 %b月份 %Y年份 %H:%M:%S时间'''
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(filename)s %(levelname)s %(message)s',
                    datefmt='%a %d %b %Y %H:%M:%S', filename='my.log', filemode='w')


def addImgToBackGround(sourceImg, centerX, centery, backImg):
    img1 = backImg
    img2 = sourceImg

    w1 = img2[:, :, 0].shape[1]
    h1 = img2[:, :, 0].shape[0]

    for x in range(centerX - int(w1 // 2), centerX + int(w1 // 2)):
        for y in range(centery - int(h1 // 2), centery + int(h1 // 2)):
            rgb_img = img2[y - 1 - (centery - int(h1 // 2)), x - 1 - (centerX - int(w1 // 2)), :]
            if rgb_img[0] < 230 or rgb_img[1] < 230 or rgb_img[2] < 230:
                img1[y, x, :] = 0
            else:
                img2[y - 1 - (centery - int(h1 // 2)), x - 1 - (centerX - int(w1 // 2)), :] = 0

            img1[y, x, :] += img2[y - 1 - (centery - int(h1 // 2)), x - 1 - (centerX - int(w1 // 2)), :]

    return img1


if __name__ == "__main__":
    '''
    target是小图存放文件夹
    background是背景图片存放文件夹
    11是最终合成图片写入的文件夹
    for p in range(1000):循环次数，需要生成多少张图片自行修改
    
    rename为最终合成图片命名格式
    rename的组成结构为：小图数量@背景图文件名前缀+小图文件名前缀-小图文件名前缀
    '''

    sourceImgList = []#存放图片名
    sourceImgnameList = []#存放图片名前缀
    for root, dirs, files in os.walk("target"):
        for fileName in files:
            sourceImgnameList.append(int(fileName.split(".")[0]))#把所有小图的文件名前缀加入sourceImgnameList列表

    sourceImgnameList.sort()#列表做升序排列
    for k in range(len(sourceImgnameList)):
        sourceImgList.append(str(sourceImgnameList[k]) + ".jpg")#将升序排列后的列表元素全部加上后缀

    #背景图同理
    backImgList = []
    backImgnameList = []
    for root, dirs, files in os.walk("background"):
        for fileName in files:
            backImgnameList.append(int(fileName.split(".")[0]))

    backImgnameList.sort()
    for q in range(len(backImgnameList)):
        backImgList.append(str(backImgnameList[q]) + ".jpg")

    for p in range(1000):
        try:
            imgnum1 = random.choice(sourceImgnameList)
            backnum = random.choice(backImgnameList)

            #读取随机选择的图片
            back = cv2.imread("background/" + backImgList[backnum])
            wh1 = cv2.imread("target/" + sourceImgList[imgnum1])

            wh11 = wh1[:, :, 0].shape[1]#获取图片的宽高
            outImg = addImgToBackGround(wh1, 500, 400, back)#以(500，400)为背景图的中心点，贴上第一张随机选择的小图
            rename = str(backnum+1) + "+" + str(imgnum1+1)#将背景图和小图前缀转化成字符串相加

            for i in range(10):

                imgnum2 = random.choice(sourceImgnameList)
                wh2 = cv2.imread("target/" + sourceImgList[imgnum2])
                wh22 = wh2[:, :, 0].shape[1]

                #定义左上角的随机坐标点x2,y2
                x2 = random.randint(250, 850)
                y2 = random.randint(200, 550)

                imgnum3 = random.choice(sourceImgnameList)
                wh3 = cv2.imread("target/" + sourceImgList[imgnum3])
                wh33 = wh3[:, :, 0].shape[1]

                # 定义右下角的随机坐标点x3,y3
                x3 = random.randint(250, 850)
                y3 = random.randint(200, 550)

                #判断左上角的随机坐标点是否跟中心坐标点相交
                if (x2 + wh22 // 2) - (500 - wh11 // 2) <= 0:
                    outImg = addImgToBackGround(wh2, x2, y2, outImg)
                    rename = rename + "-" + str(imgnum2 + 1)
                elif (y2 + wh22 // 2) - (400 - wh11 // 2) <= 0:
                    outImg = addImgToBackGround(wh2, x2, y2, outImg)
                    rename = rename + "-" + str(imgnum2 + 1)
                else:
                    break

                #判断右下角的随机坐标点是否跟中心坐标点相交，以及是否跟x2,y2相交
                if ((500 + wh11 // 2) - (x3 - wh33 // 2)) <= 0 and ((y2 + wh22 // 2)-(y3 - wh33 // 2)) <= 0:
                    outImg = addImgToBackGround(wh3, x3, y3, outImg)
                    rename = rename + "-" + str(imgnum3 + 1)
                elif ((400 + wh11 // 2) - (y3 - wh33 // 2)) <= 0 and ((x2 + wh22 // 2)-(x3 - wh33 // 2)) <= 0:
                    outImg = addImgToBackGround(wh3, x3, y3, outImg)
                    rename = rename + "-" + str(imgnum3 + 1)
                else:
                    break

            rename=str(rename.count("-")+1) + "@" + rename

            if "-" in rename:#判断贴图的数量，若贴图数量为1则不写入
                cv2.imwrite("save/%s.jpg" % rename, outImg)
                print("成功")
            else:
                print("del")

        except IndexError as error:#出现异常写入my.log中
            logging.error('this is error')