import os
import shutil


for root, dirs, files in os.walk("save"):
    for fileName in files:
        try:
            shutil.move(root+'/'+fileName,"background1/11")
        except Exception as error:
            print("{}移动失败".format(fileName))
print("-------------文件移动成功-------------")


for root, dirs, files in os.walk("background1/11"):
    count=158
    for fileName in files:
        try:
            # # 获取图片前缀
            # fileNameInitial=fileName.split('.jpg')[0]
            shutil.move(root+'/'+fileName,root+"/{}.jpg".format(count))
            count=count+1
        except Exception as error:
            print("{}重命名失败".format(fileName))
print("-------------target文件夹里图片重命名成功-------------")
