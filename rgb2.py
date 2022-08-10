from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os


def whiteToBlack(imgPath,imgName):
    img = Image.open(imgPath)
    arr = np.asarray(img)
    arr1 =arr.copy()
    for i in arr1:
        for j in i:
            if (200<=j[0]<=255 and 200<=j[1]<=255 and 240<=j[2]<=255):
                j[0] = 0
                j[1] = 0
                j[2] = 0
    plt.imsave('22/'+imgName,arr1)



for root,dirs,files in os.walk("2"):
    for fileName in files:
        whiteToBlack(root+"/"+fileName,fileName)