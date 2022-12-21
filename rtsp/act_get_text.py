from PIL import Image
import pytesseract
import cv2
import os

image = cv2.imread('test4.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
result = cv2.equalizeHist(gray)
# gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]  # 二值化操作
#
# filename = "{}.png".format(os.getpid())
# cv2.imwrite(filename, gray)  # 在当前文件中创建新文件，把gray数据写入filename路径中

text = pytesseract.image_to_string(result,lang='chi_sim')
# 识别中文，不加lang='chi_sim'默认识别英文
# image_to_string将图像上的Tesseract OCR运行结果返回到字符

print(text)

data = []
for j in list(text):
    if j.isdigit():
        data.append(j)
data = data[:14]
print(data)
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
    print("deal_datatime error!")

#os.remove(filename)  # 删除指定路径的文件

# cv2.imshow("Image", image)
cv2.imshow("Output", result)
cv2.waitKey(0)
