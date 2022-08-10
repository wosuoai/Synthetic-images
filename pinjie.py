import cv2
import numpy as np
import glob as glob
import os

num = 9
os.chdir(r"G:\moveRename\save")
img_name = []
for file_name in glob.glob("*.jpg"):
    print(file_name)
    img_name.append(file_name)

# 批量处理图片
img_path = glob.glob("G:/moveRename/save/*jpg")
for i in range(int(len(img_path) / num)):
    path = img_path[i * num]
    print(path)
    img_out = cv2.imread(path)

    for j in range(1, num):
        path = img_path[i * num + j]
        img_tmp = cv2.imread(path)

        #img_out = np.concatenate((img_out, img_tmp), axis=1)
        img_out = np.concatenate((img_out, img_tmp))

    # cv2.imshow("IMG", img_out)
    cv2.imwrite("G:/moveRename/save1/" + img_name[i * num + j][0:-6] + ".jpg", img_out)