# -*- coding=GBK -*-

import cv2 as cv

import numpy as np

from fgqy.fg_test import fg_run


def run_fgqy(src, style, index_lists):
    img = cv.imread(src)
    x_min = min(index_lists[0])
    x_max = max(index_lists[0])
    y_min = min(index_lists[1])
    y_max = max(index_lists[1])
    print('x_min, y_min', x_min, y_min)
    img_part = img[x_min: x_max, y_min: y_max]
    part_src = fg_run(style, img_part)
    result_img = cv.imread(part_src)
    # rows, cols, tun = result_img.shape
    for index in range(len(index_lists[0])):
        x = index_lists[0][index]
        y = index_lists[1][index]
        for c in range(3):
            img[x, y, c] = result_img[x - x_min, y - y_min, c]
    cv.imwrite(src, img)


if __name__ == '__main__':
    lists = [[] for i in range(2)]
    right = 1500
    left = 1500
    for i in range(100, 300):
        for j in range(left, right):
            lists[0].append(i)
            lists[1].append(j)
        if left > 1200:
            left -= 1
        if right < 1800:
            right += 1
    left = 1200
    right = 1800
    for i in range(400, 600):
        for j in range(left, right):
            lists[0].append(i)
            lists[1].append(j)
        if left < 1500:
            left += 1
        if right > 1500:
            right -= 1

    print(lists[0])
    print(lists[1])
    print(len(lists[0]))
    run_fgqy('image_content/bizhi2.jpg', 'wave', lists)

# 用一个二维数组存储每个像素点的坐标。对截图的部分进行处理后，在填充回指定位置
