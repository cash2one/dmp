#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
DMP (Data Manager Platform)
有如下几个概念:
text    输入文本. 还没有切分成词的列表.
doc     文档. 已经通过 split 函数切分成词的列表了.
bow     bag-of-word. 词袋, 已经切分并去重统计词频的列表, 格式为 (词, 词频).
'''
from gensim.corpora import Dictionary
from gensim.models import LdaModel
import sys
import codecs
import libs


config = libs.get_config()


class DMP(object):

    def __init__(self):
        self.dic = None
        self.lda = None
        self.topic_num = config.getint('dmp', 'topic_num')
        self.corpus_file = config.get('dmp', 'corpus_file')

    @staticmethod
    def __text2doc(iterator, sep=u' '):
        '''将文本转换为文档
        通过 split 函数将文本切成词的列表.

        参数
            sep: 分隔符

        返回
            返回已经切割好的词的列表
        '''
        docs = []
        for line in iterator:
            text = line.strip().split(sep)
            docs.append(text)
        return docs

    def __load_corpus(self):
        '''读取语料. 通过调用 text2doc 将文本转换为词的列表.

        返回
            返回处理过后的文档的列表.
        '''
        docs = None
        with codecs.open(self.corpus_file, 'r', 'utf-8') as iterator:
            docs = self.__text2doc(iterator)
        return docs

    def train(self):
        '''训练模型, 将会得到词典 (dic) 和模型 (lda) 两个对象.

        dic: 用来存储词, 每个词会有一个编号. 可以通过 dic[id] 来获取词
        lda: 模型, 包含主题的列表. 每个主题有一个编号, 可以通过
             lda.print_topic(id) 来获取主题中词的列表
        '''
        docs = self.__load_corpus()
        self.dic = Dictionary(docs)
        bow = [self.dic.doc2bow(doc) for doc in docs]
        self.lda = LdaModel(bow, id2word=self.dic,
                            num_topics=self.topic_num)

    def infer(self, doc):
        '''推断新的文档是什么主题

        参数
            doc: 新的文档. 要以词的列表的形式呈现

        返回
            返回主题列表的迭代器, 其中主题均采用编号呈现, 需调用 lda.print_topic
            函数来方便人工理解.
        '''
        bow = self.dic.doc2bow(doc)
        topics = self.lda[bow]
        return topics

    def dump(self):
        '''导出 lda 模型和 dic 词典.
        '''
        lda_file = config.get('dmp', 'lda_file')
        dic_file = config.get('dmp', 'dic_file')
        self.lda.save(lda_file)
        self.dic.save(dic_file)

    def load(self):
        '''读取 lda 模型和 dic 词典.
        '''
        lda_file = config.get('dmp', 'lda_file')
        dic_file = config.get('dmp', 'dic_file')
        self.lda = LdaModel.load(lda_file)
        self.dic = Dictionary.load(dic_file)


if __name__ == '__main__':
    dmp = DMP()
    '''
    dmp.train()
    topics = dmp.infer([u'dog', u'kills', u'cat', u'and', u'dog'])
    for topic_id, probability in topics:
        print dmp.lda.print_topic(topic_id), probability
    dmp.dump()
    '''
    dmp.load()
    topics = dmp.infer([u'dog', u'kills', u'cat', u'and', u'dog'])
    for topic_id, probability in topics:
        print dmp.lda.print_topic(topic_id), probability

