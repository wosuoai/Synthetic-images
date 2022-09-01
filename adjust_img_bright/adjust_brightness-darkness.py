from PIL import Image
from skimage import exposure, img_as_float, io
import os


for root, dirs, files in os.walk("1111"):
    for file in files:
        pic_path = os.path.join(root, file)  #每一个图片的绝对路径

        img_org = Image.open(pic_path)# 读取图像
        img = img_as_float(img_org)# 转换为 skimage 可操作的格式

        # 调整图像亮度，数值低于1.0表示调亮，高于1.0表示调暗。
        img_light = exposure.adjust_gamma(img, 0.7)
        img_dark = exposure.adjust_gamma(img, 1.5)


        io.imsave(os.path.join("1/", file[:-4] + "-light.jpg"),img_light)
        io.imsave(os.path.join("1/", file[:-4] + "-dark.jpg"),img_dark)
