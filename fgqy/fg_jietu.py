# -*- coding=GBK -*-

import cv2 as cv

import numpy as np

from fgqy.fg_test import fg_run


# ����ͼ����Ǩ��ʵ��
def cut_by_rectangle(src1, style, start_x, start_y, end_x, end_y):
    img1 = cv.imread(src1)  # ԭʼͼ��
    image_part = img1[start_x:end_x, start_y:end_y]  # ��ȡ��start_x�е�end_x�еĵ�start_y�е�end_y�е�����
    fgqi_result = fg_run(style, image_part)
    img2 = cv.imread(fgqi_result)  # ������ͼ��Ҫ��ԭʼͼ�������
    # img2 = cv.resize(img2, ((end_y - start_y), (end_x - start_x)))
    roi = img1[start_x:end_x, start_y:end_y]  # ��ԭʼͼ���н�ȡimg2ͼ���С�Ĳ���

    img2gray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)  # ��img2ͼ��ҶȻ�
    ret, mask = cv.threshold(img2gray, 200, 255, cv.THRESH_BINARY)  # ��img2�Ҷ�ͼ��ֵ�������õ���ͼ��ֵ��mask��img2���ֵ�ֵΪ255����ɫ
    mask_inv = cv.bitwise_not(mask)  # ��mask��λȡ�������ױ�ڣ��ڱ��

    img1_bg = cv.bitwise_and(roi, roi, mask=mask)  # ��ԭʼͼ���н�ȡ�Ĳ���������mask�к�ɫ���ְ�λ�����㣬��������ɫ���֣�������img2λ����Ĳ���
    img2_fg = cv.bitwise_and(img2, img2, mask=mask_inv)

    dst = cv.add(img1_bg, img2_fg)  # ͼ�����
    img1[start_x:end_x, start_y:end_y] = dst  # ͼ���滻
    cv.imwrite(src1, img1)


# �Դ���������������ͼ����Ǩ�� ����Ҫ��ô�鷳��ֱ�ӷ��Ǩ�ƺ󣬽����ɵķ��Ǩ�Ʋ���
# ��ÿ�����أ����������滻��ԭͼ���м���
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
#     mask_inv = cv.bitwise_not(mask)  # ��mask��λȡ�������ױ�ڣ��ڱ��
#     img1_bg = cv.bitwise_and(pixelArrays, pixelArrays, mask=mask)
#     img2_fg = cv.bitwise_and(new_part_img, new_part_img, mask=mask_inv)
#     dst = cv.add(img1_bg, img2_fg)  # ͼ�����
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

# ͼ�����鲢û�м�¼ʵ���ϵ�����ֵ�����磬img = img[300, 600, 100, 600]
# ���ɵ�ͼ�������Ǵ� row �� 300-600�� �д�100-600��ÿ��������ͨ����ɫֵ��ͼ��
# ��һ����ά����洢ÿ�����ص�����ꡣ�Խ�ͼ�Ĳ��ֽ��д����������ָ��λ��
