# -*- coding=GBK -*-

import cv2 as cv
import random
import numpy as np

from fgqy.fg_test import fg_run


def run_fgqy(src, style, index_lists):
    """
     风格迁移方法：
     @src: 原图片路径
     @style: 指定迁移风格
     @index_list: 待迁移区域的坐标数组
    """
    img = cv.imread(src)
    x_min = min(index_lists[0])
    x_max = max(index_lists[0])
    y_min = min(index_lists[1])
    y_max = max(index_lists[1])
    print('x_min, x_max, y_min, y_max', x_min, x_max, y_min, y_max)
    img_part = img[x_min: x_max, y_min: y_max]
    part_src = fg_run(style, img_part)
    result_img = cv.imread(part_src)
    rows, cols, tun = result_img.shape
    print('rows = %d, cols = %d, tun = %d', (rows, cols, tun))
    for index in range(len(index_lists[0])):
        x = index_lists[0][index]
        y = index_lists[1][index]
        for c in range(3):
            img[x, y, c] = result_img[x - 1 - x_min , y - y_min - 1 , c]
    cv.imwrite(src, img)


if __name__ == '__main__':
    lists = [[] for i in range(2)]
    for i in range(300, 700):
        if i % 2 == 0:
            left = 200 + random.randint(100, 299)
            right = 500 + random.randint(0, 100)
        else:
            left = 500 - random.randint(0, 50)
            right = 700 - random.randint(0, 200)

        for j in range(left, right):
            lists[0].append(i)
            lists[1].append(j)

    print(lists[0])
    print(lists[1])
    print(len(lists[0]))
    print(len(lists[1]))
    run_fgqy('image_content/bizhi1.jpg', 'muse', lists)

# 用一个二维数组存储每个像素点的坐标。对截图的部分进行处理后，在填充回指定位置
