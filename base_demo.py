# -*- coding: utf-8 -*-
"""
@author:XuMing(xuming624@qq.com)
@description:
"""

import sys

sys.path.append("..")

import pycorrector

if __name__ == '__main__':
    pyc = pycorrector.Corrector()
    corrected_sent, detail = pyc.correct('少先队员english因该为老人让坐，我想要喝税')
    print(corrected_sent, detail)

    error_sentences = [
        '真麻烦你了。python希望你们好好的跳无',
        '机七学习是人工智能领遇最能体现智能的一个分知',
        '一只小鱼船浮在平净的河面上',
        '我的家乡是有明的渔米之乡,caijingxinwen',
        '财经心闻，我想要喝税'
    ]
    for line in error_sentences:
        correct_sent, err = pycorrector.correct(line)
        print("{} => {} {}".format(line, correct_sent, err))