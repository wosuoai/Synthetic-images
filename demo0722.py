import cv2

img1 = cv2.imread(r'background.jpg')
# w = img1[:, :, 0].shape[1]
# h = img1[:, :, 0].shape[0]
img2 = cv2.imread(r'G:/moveRename/save/1.jpg')
#img2 = cv2.resize(img2, (300, 300))
w1 = img2[:, :, 0].shape[1]
h1 = img2[:, :, 0].shape[0]

centerX = 500
centery = 500


# for x in range(w):
#     for y in range(h):
#         if x in range(centerX - int(w1 / 2), centerX + int(w1 / 2)) and y in range(centery - int(h1 / 2), centery + int(h1 / 2)):
#             rgb_img = img2[y - 1 - (centery - int(h1 // 2)), x - 1 - (centerX - int(w1 // 2)), :]
#             if rgb_img[0] > 250 or rgb_img[1] > 250 or rgb_img[2] > 20:
#                 img1[y, x, :] = 0
#             else:
#                 continue
#
#             img1[y, x, :] += img2[y - 1 - (centery - int(h1 // 2)), x - 1 - (centerX - int(w1 // 2)), :]
#         else:
#             continue

for x in range(centerX - int(w1 / 2), centerX + int(w1 / 2)):
    for y in range(centery - int(h1 / 2), centery + int(h1 / 2)):
        # if x in range(centerX - int(w1 / 2), centerX + int(w1 / 2)) and y in range(centery - int(h1 / 2),  centery + int(h1 / 2)):
        rgb_img = img2[y - 1 - (centery - int(h1 // 2)), x - 1 - (centerX - int(w1 // 2)), :]
        if rgb_img[0] > 250 or rgb_img[1] > 250 or rgb_img[2] > 10:
            img1[y, x, :] = 0
        else:
            continue

        img1[y, x, :] += img2[y - 1 - (centery - int(h1 // 2)), x - 1 - (centerX - int(w1 // 2)), :]
        # else:
        #     continue


cv2.imshow('img1', img1)
cv2.waitKey(0)
cv2.destroyAllWindows()