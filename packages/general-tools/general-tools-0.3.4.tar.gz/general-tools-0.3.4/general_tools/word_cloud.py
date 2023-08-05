#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Author: xuwei
Email: 18810079020@163.com
File: answer_prequestions.py
Date: 2020/4/13 9:57 上午
'''

import jieba
import os
from imageio import imread
import jieba.analyse as analyse
from wordcloud import WordCloud

# from scipy.misc import imread
# import matplotlib.pyplot as plt

"""
wordcloud生成中文词云
"""


class WordCloudFactory(object):

    def __init__(self, text_file_path='', background_image_path='', save_image_path='',
                 background_color='white', width=200, height=200, max_words=2000, max_font_size=40):
        self.background_color = background_color
        self.width = width
        self.height = height
        self.max_words = max_words
        self.max_font_size = max_font_size
        self.text_file_path = text_file_path
        self.background_image_path = background_image_path
        self.save_image_path = save_image_path

    # 绘制词云
    def draw_image(self):
        # 读入一个txt文件
        comment_text = open(self.text_file_path, 'r', encoding='utf-8').read()
        # 结巴分词，生成字符串，如果不通过分词，无法直接生成正确的中文词云
        cut_text = " ".join(jieba.cut(comment_text))
        color_mask = imread(self.background_image_path)  # 读取背景图片
        current_dir = os.path.dirname(os.path.abspath(__file__)) # 获取当前代码路径
        cloud = WordCloud(
            # 设置字体，不指定就会出现乱码
            font_path=current_dir + "/fonts/Simfang.ttf",
            width=self.width,
            height=self.height,
            background_color=self.background_color,  # 设置背景色
            mask=color_mask,  # 词云形状
            max_words=self.max_words,  # 允许最大词汇
            max_font_size=self.max_font_size  # 最大号字体
        )
        word_cloud = cloud.generate(cut_text)
        word_cloud.to_file(self.save_image_path)  # 保存图片


if __name__ == '__main__':
    wordCloudFactory = WordCloudFactory(text_file_path='./word_cloud/static/test.txt',
                                        background_image_path='./word_cloud/static/images/alice.png',
                                        save_image_path='./test.jpg')
    wordCloudFactory.draw_image()
