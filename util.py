"""汉字处理的工具:
判断unicode是否是汉字，数字，英文，或者其他字符。
全角符号转半角符号。"""
from pyparsing import unichr
import jieba

def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if u'\u4e00' <= uchar <= u'\u9fa5':
        return True
    else:
        return False


def is_number(uchar):
    """判断一个unicode是否是数字"""
    if u'\u0030' <= uchar <= u'\u0039':
        return True
    else:
        return False


def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if (u'\u0041' <= uchar <= u'\u005a') or (u'\u0061' <= uchar <= u'\u007a'):
        return True
    else:
        return False


def is_other(uchar):
    """判断是否非汉字，数字和英文字符"""
    if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
        return True
    else:
        return False


def judge_char(uchar):
    if is_chinese(uchar):
        return 'c'
    elif is_alphabet(uchar):
        return 'e'
    elif is_number(uchar):
        return 'n'
    else:
        return 'o'


def B2Q(uchar):
    """半角转全角"""
    inside_code = ord(uchar)
    if inside_code < 0x0020 or inside_code > 0x7e:  # 不是半角字符就返回原来的字符
        return uchar
    if inside_code == 0x0020:  # 除了空格其他的全角半角的公式为:半角=全角-0xfee0
        inside_code = 0x3000
    else:
        inside_code += 0xfee0
    return unichr(inside_code)


def Q2B(uchar):
    """全角转半角"""
    inside_code = ord(uchar)
    if inside_code == 0x3000:
        inside_code = 0x0020
    else:
        inside_code -= 0xfee0
    if inside_code < 0x0020 or inside_code > 0x7e:  # 转完之后不是半角字符返回原来的字符
        return uchar
    return unichr(inside_code)


def stringQ2B(ustring):
    """把字符串全角转半角"""
    return "".join([Q2B(uchar) for uchar in ustring])


def uniform(ustring):
    """格式化字符串，完成全角转半角，大写转小写的工作"""
    return stringQ2B(ustring).lower()


def string2List(ustring):
    """将ustring按照中文，字母，数字分开"""
    retList = []
    utmp = []
    for uchar in ustring:
        if is_other(uchar):
            if len(utmp) == 0:
                continue
            else:
                retList.append("".join(utmp))
                utmp = []
        else:
            utmp.append(uchar)
    if len(utmp) != 0:
        retList.append("".join(utmp))
    return retList


def split_query(ustring):
    """
    cn c
    en e
    num n
    other o
    Args:
        ustring:

    Returns:

    """
    length = len(ustring)
    return_list = []
    utmp = []
    flag = ''
    for unum, uchar in enumerate(ustring):
        if flag == '':
            utmp.append(uchar)
            flag = judge_char(uchar)
        else:
            flag_t = judge_char(uchar)
            if flag_t == flag:
                utmp.append(uchar)
            else:
                return_list.append("".join(utmp))
                utmp = [uchar]
                flag = flag_t

        if unum == length - 1:
            return_list.append("".join(utmp))
            return return_list


def uniform_and_split(ustring):
    """
    全角转半角，英文全部变成小写， 然后再进行拆分
    Args:
        ustring:

    Returns:

    """
    return split_query(uniform(ustring))


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

# jieba.enable_paddle()# 启动paddle模式。 0.40版之后开始支持，早期版本不支持
# strs=["我来到北京清华大学","乒乓球拍卖完了","中国科学技术大学"]
# for str in strs:
#     seg_list = jieba.cut(str,use_paddle=True) # 使用paddle模式
#     print("Paddle Mode: " + '/'.join(list(seg_list)))

# seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
# print("Full Mode: " + "/ ".join(seg_list))  # 全模式
#
# seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
# print("Default Mode: " + "/ ".join(seg_list))  # 精确模式
#
# seg_list = jieba.cut("他来到了网易杭研大厦")  # 默认是精确模式
# print(", ".join(seg_list))
#
# seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
# print(", ".join(seg_list))



if __name__ == "__main__":
    # test Q2B and B2Q
    # for i in range(0x0020, 0x007F):
    #     print(Q2B(B2Q(unichr(i))), B2Q(unichr(i)))

    # test uniform
    ustring = u'中国 人名ａbbbb123高频Ａ'
    # ustring = uniform(ustring)
    # print(ustring)
    # ret = split_query(ustring)
    # print(ret)
    print(uniform_and_split(ustring))

    text = "小明硕士毕业于python123中国科学院计算所，后在日本京都大学深造"
    print(jieba_divide(text, "all"))
    print(jieba_divide(text, "precision"))
    print(jieba_divide(text, "search"))
