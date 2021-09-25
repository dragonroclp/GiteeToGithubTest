# pinyin_and_correction
 词、句拼音转汉字、拼音分割、拼音补全、汉字纠错、文本纠错、文本分词

split_pinyin.py实现的是拼音分割，输出结果包括完美分割、可补全、其他三类，借鉴了[这里](https://blog.csdn.net/songrps/article/details/103591422/)的代码。


my_pinyin2hanzi.py实现的是词、句拼音转汉字，基于[Pinyin2Hanzi](https://github.com/letiantian/Pinyin2Hanzi)。


base_demo.py 纠错示例


util.py  拼音转汉字、文本纠错工具


thrift_demo.py  thrift服务启动类


flask  曾经实现的http接口


thrift  .thrift文件


correctorservice   thrift生成的类
