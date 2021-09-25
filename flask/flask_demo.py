import flask
from flask import Flask, request, Response
import pycorrector
from util import is_number, is_alphabet, is_chinese, is_other, uniform_and_split
from my_pinyin2hanzi import Pinyin2Hanzi
import jieba
import json


app = Flask(__name__)

# 初始化一个类
pyc = pycorrector.Corrector()
pin2han = Pinyin2Hanzi()
jieba.initialize()


# 结巴分词
def jieba_divide(text, way):
    """

    Args:
        text:
        way: all 全模式  precision 精确模式  search 搜索模式

    Returns:

    """
    if way == "all":
        return jieba.lcut(text, cut_all=True)
    elif way == "precision":
        return jieba.lcut(text, cut_all=False)
    elif way == "search":
        return jieba.lcut_for_search(text)


# http://127.0.0.1:5000/correction?text=喝税

@app.route('/correction', methods=['GET'])
def correct():
    """
    1. 先将query进行全角转半角， 并拆分成4类不同的字段
    2. 判断每一个字段属于哪个类
    3. 对于拼音进行转汉字，然后对所有的汉字进行纠错
    Returns:

    """
    text = request.args["text"]
    way = request.args["way"]
    corrected_list = []
    list_return = []
    print(text)
    # 先将搜索的句子进行全角转半角，大写转小写，并进行汉字拼音拆分
    text_divided_list = uniform_and_split(text)
    print(text_divided_list)
    for divided_part_num, divided_part in enumerate(text_divided_list):
        first_char = divided_part[0]
        if is_chinese(first_char):
            corrected_text, detail = pyc.correct(divided_part)
            corrected_list.append(corrected_text)
            list_return += jieba_divide(corrected_text, way)
        elif is_alphabet(first_char):
            cn = pin2han.get_one(divided_part)
            print("cn为")
            print(cn)
            if cn != "error":
                corrected_list.append(cn)
                list_return += jieba_divide(cn, way)
            else:
                corrected_list.append(divided_part)
                list_return.append(divided_part)
        else:
            corrected_list.append(divided_part)
            list_return.append(divided_part)

    # # 调用类的方法
    # corrected_text, detail = pyc.correct(text)
    # print(corrected_text, detail)
    # print("===")
    # print(corrected_text)
    print(corrected_list)
    print(list_return)
    # 编码转换
    # list_return_utf8 = [s.encode('utf8') for s in list_return]
    # print("编码后")
    # print(list_return_utf8)
    rt = {"init_text": text, "init_divided": text_divided_list, "init_corrected": corrected_list,
          "divided_text": list_return, "way": way}
    return Response(json.dumps(rt, ensure_ascii=False), mimetype='application/json')


app.config['JSON_AS_ASCII'] = False
app.run()