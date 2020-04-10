# -*- coding=GBK -*-

import cv2 as cv

import numpy as np

from fgqy.fg_test import fg_run


# ����ͼ����Ǩ��ʵ��
def cut_by_rectangle(src1, style, start_x, start_y, end_x, end_y):
    img1 = cv.imread(src1)  # ԭʼͼ��
    image_part = img1[start_x:end_x, start_y:end_y]  # ��ȡ��5�е�89�еĵ�500�е�630�е�����
    fgqi_result = fg_run(style, image_part)
    img2 = cv.imread(fgqi_result)  # logoͼ��Ҫ��ԭʼͼ��������
    # img2 = cv.resize(img2, ((end_y - start_y), (end_x - start_x)))
    roi = img1[start_x:end_x, start_y:end_y]  # ��ԭʼͼ���н�ȡlogoͼ���С�Ĳ���

    img2gray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)  # ��logoͼ��ҶȻ�
    ret, mask = cv.threshold(img2gray, 200, 255, cv.THRESH_BINARY)  # ��logo�Ҷ�ͼ��ֵ�������õ���ͼ��ֵ��mask��logo���ֵ�ֵΪ255����ɫ
    mask_inv = cv.bitwise_not(mask)  # ��mask��λȡ�������ױ�ڣ��ڱ��

    img1_bg = cv.bitwise_and(roi, roi, mask=mask)  # ��ԭʼͼ���н�ȡ�Ĳ�����������mask�к�ɫ���ְ�λ�����㣬��������ɫ���֣�������logoλ����Ĳ���
    img2_fg = cv.bitwise_and(img2, img2, mask=mask_inv)  # ��logoͼ���У�mask_inv���ְ�λ�����㣬��������ɫ���֣�����logo

    dst = cv.add(img1_bg, img2_fg)  # ͼ�����
    img1[start_x:end_x, start_y:end_y] = dst  # ͼ���滻
    cv.imwrite(src1, img1)


def cut_with_pixelArrays(src, style, pixelArrays):
    srcImage = cv.imread(src)
    new_part_img = fg_run(style, pixelArrays)
    # new_part_img = cv.imread(fgqy_part_img)
    # rows, cols, tun = new_part_img.shape
    # print('row = %d, col = %d, tun = %d', rows, cols, tun)
    img2gray = cv.cvtColor(new_part_img, cv.COLOR_BGR2GRAY)
    ret, mask = cv.threshold(img2gray, 200, 255, cv.THRESH_BINARY)
    mask_inv = cv.bitwise_not(mask)  # ��mask��λȡ�������ױ�ڣ��ڱ��
    img1_bg = cv.bitwise_and(pixelArrays, pixelArrays, mask=mask)  # ��ԭʼͼ���н�ȡ�Ĳ�����������mask�к�ɫ���ְ�λ�����㣬��������ɫ���֣�������logoλ����Ĳ���
    img2_fg = cv.bitwise_and(new_part_img, new_part_img, mask=mask_inv)  # ��logoͼ���У�mask_inv���ְ�λ�����㣬��������ɫ���֣�����logo

    dst = cv.add(img1_bg, img2_fg)  # ͼ�����
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