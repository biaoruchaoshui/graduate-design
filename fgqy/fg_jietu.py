# -*- coding=GBK -*-

import cv2 as cv

import numpy as np

from fgqy.fg_test import fg_run


# 矩形图像风格迁移实现
def cut_by_rectangle(src1, style, start_x, start_y, end_x, end_y):
    img1 = cv.imread(src1)  # 原始图像
    image_part = img1[start_x:end_x, start_y:end_y]  # 截取第start_x行到end_x行的第start_y列到end_y列的区域
    fgqi_result = fg_run(style, image_part)
    img2 = cv.imread(fgqi_result)  # 待覆盖图像，要往原始图像上添加
    # img2 = cv.resize(img2, ((end_y - start_y), (end_x - start_x)))
    roi = img1[start_x:end_x, start_y:end_y]  # 在原始图像中截取img2图像大小的部分

    img2gray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)  # 将img2图像灰度化
    ret, mask = cv.threshold(img2gray, 200, 255, cv.THRESH_BINARY)  # 将img2灰度图二值化，将得到的图像赋值给mask，img2部分的值为255，白色
    mask_inv = cv.bitwise_not(mask)  # 将mask按位取反，即白变黑，黑变白

    img1_bg = cv.bitwise_and(roi, roi, mask=mask)  # 将原始图像中截取的部分做处理，mask中黑色部分按位与运算，即保留黑色部分，保留除img2位置外的部分
    img2_fg = cv.bitwise_and(img2, img2, mask=mask_inv)

    dst = cv.add(img1_bg, img2_fg)  # 图像相加
    img1[start_x:end_x, start_y:end_y] = dst  # 图像替换
    cv.imwrite(src1, img1)


def cut_with_pixelArrays(src, style, pixelArrays):
    srcImage = cv.imread(src)
    new_part_img = fg_run(style, pixelArrays)
    # new_part_img = cv.imread(fgqy_part_img)
    # rows, cols, tun = new_part_img.shape
    # print('row = %d, col = %d, tun = %d', rows, cols, tun)
    img2gray = cv.cvtColor(new_part_img, cv.COLOR_BGR2GRAY)
    ret, mask = cv.threshold(img2gray, 200, 255, cv.THRESH_BINARY)
    mask_inv = cv.bitwise_not(mask)  # 将mask按位取反，即白变黑，黑变白
    img1_bg = cv.bitwise_and(pixelArrays, pixelArrays, mask=mask)
    img2_fg = cv.bitwise_and(new_part_img, new_part_img, mask=mask_inv)
    dst = cv.add(img1_bg, img2_fg)  # 图像相加
    rows, cols, tun = dst.shape
    print('row = %d, col = %d, tun = %d', rows, cols, tun)
    for row in range(rows):
        for col in range(cols):
            for c in range(tun):
                srcImage[row, col, c] = dst[row, col, c]
    cv.imwrite(src, srcImage)


if __name__ == '__main__':
    # cut_by_rectangle('content_image/place.jpg', 'wave', 0, 0, 500, 600)
    img = cv.imread('content_image/place.jpg')
    img = img[300: 600, 100: 600]
    cut_with_pixelArrays('content_image/place.jpg', 'muse', img)
