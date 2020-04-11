# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np
from scipy.misc import imread, imsave
import os
import time
import cv2 as cv


def the_current_time():
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time()))))


# 图片风格迁移方法 style:迁移风格， content_image： 内容图片
def  fg_run(style, X_image):
    model = 'saver_%s' % style
    result_image = 'image_output/test_%s.jpg' % style

    sess = tf.Session()
    sess.run(tf.global_variables_initializer())

    saver = tf.train.import_meta_graph(os.path.join(model, 'fast_style_transfer.meta'))
    saver.restore(sess, tf.train.latest_checkpoint(model))

    graph = tf.get_default_graph()
    X = graph.get_tensor_by_name('X:0')
    g = graph.get_tensor_by_name('transformer/g:0')
    # 开始时间
    the_current_time()

    gen_img = sess.run(g, feed_dict={X: [X_image]})[0]
    gen_img = np.clip(gen_img, 0, 255) / 255.
    imsave(result_image, gen_img)
    # 结束时间
    the_current_time()
    return gen_img



if __name__ == '__main__':
    image = fg_run('muse', 'content_image/test1.jpg')
