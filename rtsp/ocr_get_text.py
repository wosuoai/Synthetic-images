from PIL import Image
import cv2
import tesserocr
import time


def binarization_file(time_img_file, black_font=False):
    '''
    description:将指定的图像二值化
    param {time_img_file:输入的图像，图像文件xxx.jpg；black_font:把黑底白字转为白底黑字}
    return {time_bin_img:二值化后的图像，Image对象}
    '''
    # cv2进行读取
    img = cv2.imread(time_img_file)
    # If your image is not already grayscale :
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 进行二值化
    threshold = 180  # to be determined
    _, img_binarized = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    # 对二值图像进行像素反转
    if (black_font):
        img_binarized = 255 - img_binarized
    # 转为Image类型
    time_bin_img = Image.fromarray(img_binarized)
    return time_bin_img


def ocr(time_bin_img):
    '''
    description:对二值图像进行OCR识别
    param {time_bin_img:二值化后的图像，Image对象}
    return {text:识别出的字符串，取[:-1]是为了去掉换行符,replace函数用于删除其中的空格}
    '''
    text = tesserocr.image_to_text(time_bin_img)
    return text[:-1].replace(" ", "")


def time2timestamp(time_str):
    '''
    description:将时间格式的字符串转为时间戳
    param {time_text:时间格式的字符串，格式为：'2019-06-03 21:19:03'}
    return {time_stamp:时间戳，整数类型}
    '''
    time_array = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    time_stamp = int(time.mktime(time_array))
    return time_stamp


if __name__ == "__main__":
    pic = "test.png"
    bin_pic = binarization_file(pic, black_font=True)
    time_text = ocr(bin_pic)
    timestamp = time2timestamp(time_text)
    print(timestamp)
