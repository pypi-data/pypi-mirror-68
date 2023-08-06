# -*- coding: UTF-8 -*-
# !/usr/bin/python
# @time     :2019/8/21 22:01
# @author   :Mo
# @function : textrank using tfidf of sklearn, pagerank of networkx


from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import networkx as nx
import jieba
import re


def cut_sentence(sentence):
    """
        分句
    :param sentence:str
    :return:list
    """
    re_sen = re.compile('[.。？！?!\n\r]')
    sentences = re_sen.split(sentence)
    return sentences


def tdidf_sim(sentences):
    """
       tfidf相似度
    :param sentences: 
    :return: 
    """
    # tfidf计算
    model = TfidfVectorizer(tokenizer=jieba.cut,
                            ngram_range=(1, 2), # 3,5
                            stop_words=[' ', '\t', '\n'],  # 停用词
                            max_features=10000,
                            token_pattern=r"(?u)\b\w+\b",  # 过滤停用词
                            min_df=1,
                            max_df=0.9,
                            use_idf=1,  # 光滑
                            smooth_idf=1,  # 光滑
                            sublinear_tf=1, )  # 光滑
    matrix = model.fit_transform(sentences)
    matrix_norm = TfidfTransformer().fit_transform(matrix)
    return matrix_norm


def textrank_tfidf(sentences, topk=6):
    """
        使用tf-idf作为相似度, networkx.pagerank获取中心句子作为摘要
    :param sentences: str, docs of text
    :param topk:int
    :return:list
    """
    # 切句子
    sentences = list(cut_sentence(sentences))
    # tf-idf相似度
    matrix_norm = tdidf_sim(sentences)
    # 构建相似度矩阵
    tfidf_sim = nx.from_scipy_sparse_matrix(matrix_norm * matrix_norm.T)
    # nx.pagerank
    sens_scores = nx.pagerank(tfidf_sim)
    # 得分排序
    sen_rank = sorted(sens_scores.items(), key=lambda x: x[1], reverse=True)
    # 保留topk个, 防止越界
    topk = min(len(sentences), topk)
    # 返回原句子和得分
    return [(sr[1], sentences[sr[0]]) for sr in sen_rank][0:topk]


if __name__ == '__main__':
    doc = "是上世纪90年代末提出的一种计算网页权重的算法。" \
          "当时，互联网技术突飞猛进，各种网页网站爆炸式增长，" \
          "业界急需一种相对比较准确的网页重要性计算方法，" \
          "是人们能够从海量互联网世界中找出自己需要的信息。" \
          "百度百科如是介绍他的思想:PageRank通过网络浩瀚的超链接关系来确定一个页面的等级。" \
          "Google把从A页面到B页面的链接解释为A页面给B页面投票，" \
          "Google根据投票来源甚至来源的来源，即链接到A页面的页面" \
          "和投票目标的等级来决定新的等级。简单的说，" \
          "一个高等级的页面可以使其他低等级页面的等级提升。" \
          "PageRank The PageRank Citation Ranking: Bringing Order to the Web，"\
          "具体说来就是，PageRank有两个基本思想，也可以说是假设，" \
          "即数量假设：一个网页被越多的其他页面链接，就越重）；" \
          "质量假设：一个网页越是被高质量的网页链接，就越重要。" \
          "总的来说就是一句话，从全局角度考虑，获取重要的信息。"
    doc = doc.encode('utf-8').decode('utf-8')
    for score_sen in textrank_tfidf(doc, 32):
        print(score_sen)
