import os
import cv2
import random


def resize_img(DATADIR, data_k, img_size):
    w = img_size[0]
    h = img_size[1]
    path = os.path.join(DATADIR, data_k)
    img_list = os.listdir(path)

    for i in img_list:
        if i.endswith('.jpg'):
            img_array = cv2.imread((path + '/' + i), cv2.IMREAD_COLOR)
            new_array = cv2.resize(img_array, (w, h), interpolation=cv2.INTER_CUBIC)
            img_name = str(i)

            save_path = path + 'new/'
            if os.path.exists(save_path):
                print(i)

                save_img = save_path + img_name
                cv2.imwrite(save_img, new_array)
            else:
                os.mkdir(save_path)
                save_img = save_path + img_name
                cv2.imwrite(save_img, new_array)


if __name__ == '__main__':
    DATADIR = "G:/down/"
    data_k = 'resize-300-400'
    img_size = [random.randint(300,400), random.randint(300,400)]
    resize_img(DATADIR, data_k, img_size)