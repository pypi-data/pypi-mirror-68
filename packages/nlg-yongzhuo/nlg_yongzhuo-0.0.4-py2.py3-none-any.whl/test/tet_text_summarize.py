# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2020/3/17 20:59
# @author  : Mo
# @function: test megre



from nlg_yongzhuo import *


doc = """PageRank算法简介。是上世纪90年代末提出的一种计算网页权重的算法! 当时，互联网技术突飞猛进，各种网页网站爆炸式增长。 业界急需一种相对比较准确的网页重要性计算方法。是人们能够从海量互联网世界中找出自己需要的信息。 百度百科如是介绍他的思想:PageRank通过网络浩瀚的超链接关系来确定一个页面的等级。 " \
              "Google把从A页面到B页面的链接解释为A页面给B页面投票。 " \
              "Google根据投票来源甚至来源的来源，即链接到A页面的页面。 " \
              "和投票目标的等级来决定新的等级。简单的说， " \
              "一个高等级的页面可以使其他低等级页面的等级提升。 " \
              "具体说来就是，PageRank有两个基本思想，也可以说是假设。 " \
              "即数量假设：一个网页被越多的其他页面链接，就越重）。 " \
              "质量假设：一个网页越是被高质量的网页链接，就越重要。 " \
              "总的来说就是一句话，从全局角度考虑，获取重要的信。 """.replace(" ", "").replace('"', '')

# fs可以填其中一个或几个 text_pronouns, text_teaser, mmr, text_rank, lead3, lda, lsi, nmf
res_score = text_summarize(doc, fs=[text_pronouns, text_teaser, mmr, text_rank, lead3, lda, lsi, nmf])
for rs in res_score:
    print(rs)
