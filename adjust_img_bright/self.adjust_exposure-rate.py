import cv2
import numpy as np
import os


def gamma_trans(img, gamma):  # gamma函数处理
    gamma_table = [np.power(x / 255.0, gamma) * 255.0 for x in range(256)]  # 建立映射表
    gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)  # 颜色值为整数
    return cv2.LUT(img, gamma_table)  # 图片颜色查表。另外可以根据光强（颜色）均匀化原则设计自适应算法。

cv2.namedWindow("demo", 0)  # 将显示窗口的大小适应于显示器的分辨率
cv2.createTrackbar('Value of Gamma', 'demo', 100, 1000, lambda x:x)  # 使用滑动条动态调节参数gamma

data_base_dir = "1111"
outfile_dir = "1"
processed_imgnumber = 0

for file in os.listdir(data_base_dir):
    read_img_name = data_base_dir + '//' + file.strip()
    image = cv2.imread(read_img_name)

    while (1):
        value_of_gamma = cv2.getTrackbarPos('Value of Gamma', 'demo')  # gamma取值
        value_of_gamma = value_of_gamma * 0.01  # 压缩gamma范围，以进行精细调整
        image_gamma_correct = gamma_trans(image, value_of_gamma)  # 2.5为gamma函数的指数值，大于1曝光度下降，大于0小于1曝光度增强
        cv2.imshow("demo", image_gamma_correct)
        k = cv2.waitKey(1)
        if k == 13:  # 按回车键确认处理、保存图片到输出文件夹和读取下一张图片
            processed_imgnumber += 1
            out_img_name = outfile_dir + '//' + file.strip()
            cv2.imwrite(out_img_name, image_gamma_correct)
            print("The number of photos which were processed is ", processed_imgnumber)
            break
