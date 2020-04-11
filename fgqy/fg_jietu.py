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


# 对传入的像素数组进行图像风格迁移 不需要这么麻烦，直接风格迁移后，将生成的风格迁移部分
# 的每个像素，按照坐标替换到原图形中即可
# def cut_with_pixelArrays(src, style, pixelArrays):
#     srcImage = cv.imread(src)
#     # new_part_img = fg_run(style, pixelArrays)
#     # new_part_img = cv.imread(fgqy_part_img)
#     new_part_img = cv.imread('output/test_muse.jpg')
#     print('new_part_img first pix: ', new_part_img[0][0])
#     rows, cols, tun = new_part_img.shape
#     # print('new_part_img :  ', rows, cols, tun)
#     # for row in range(rows):
#     #     for col in range(cols):
#     #             new_part_img[row, col] = pixelArrays[row, col]
#     img2gray = cv.cvtColor(new_part_img, cv.COLOR_BGR2GRAY)
#     ret, mask = cv.threshold(img2gray, 200, 255, cv.THRESH_BINARY)
#     mask_inv = cv.bitwise_not(mask)  # 将mask按位取反，即白变黑，黑变白
#     img1_bg = cv.bitwise_and(pixelArrays, pixelArrays, mask=mask)
#     img2_fg = cv.bitwise_and(new_part_img, new_part_img, mask=mask_inv)
#     dst = cv.add(img1_bg, img2_fg)  # 图像相加
#     rows, cols, tun = dst.shape
#     # print('dst :  ', rows, cols, tun)
#     for row in range(rows):
#         for col in range(cols):
#             for c in range(tun):
#                 srcImage[row, col, c] = dst[row, col, c]
#     cv.imwrite(src, srcImage)


def test_fgqy(src1, src2):
    img1 = cv.imread(src1)
    img2 = cv.imread(src2)
    rows, cols, tun = img2.shape
    for row in range(rows):
        for col in range(cols):
            for c in range(tun):
                img1[row+ 600, col +600, c] = img2[row, col, c]
    cv.imwrite(src1, img1)


if __name__ == '__main__':
    # cut_by_rectangle('content_image/place.jpg', 'wave', 0, 0, 500, 600)
    img = cv.imread('image_content/bizhi1.jpg')
    img = img[600: 1200, 600: 1500]
    # rows, cols, tun = img.shape
    # print('pixArray: first pix: ', img)
    # print('pixArray :  ', rows, cols, tun)
    fg_run('muse', img)
    test_fgqy('image_content/bizhi1.jpg', 'image_output/test_muse.jpg')

# 图像数组并没有记录实际上的坐标值，比如，img = img[300, 600, 100, 600]
# 生成的图像数组是从 row 从 300-600， 列从100-600，每个点有三通道颜色值的图像
# 用一个二维数组存储每个像素点的坐标。对截图的部分进行处理后，在填充回指定位置
