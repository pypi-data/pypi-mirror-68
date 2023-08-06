# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2020/1/3 22:45
# @author  : Mo
# @function:


from nlg_yongzhuo import *

doc = """PageRank算法简介。" \
              "是上世纪90年代末提出的一种计算网页权重的算法! " \
              "当时，互联网技术突飞猛进，各种网页网站爆炸式增长。 " \
              "业界急需一种相对比较准确的网页重要性计算方法。 " \
              "是人们能够从海量互联网世界中找出自己需要的信息。 " \
              "百度百科如是介绍他的思想:PageRank通过网络浩瀚的超链接关系来确定一个页面的等级。 " \
              "Google把从A页面到B页面的链接解释为A页面给B页面投票。 " \
              "Google根据投票来源甚至来源的来源，即链接到A页面的页面。 " \
              "和投票目标的等级来决定新的等级。简单的说， " \
              "一个高等级的页面可以使其他低等级页面的等级提升。 " \
              "具体说来就是，PageRank有两个基本思想，也可以说是假设。 " \
              "即数量假设：一个网页被越多的其他页面链接，就越重）。 " \
              "质量假设：一个网页越是被高质量的网页链接，就越重要。 " \
              "总的来说就是一句话，从全局角度考虑，获取重要的信。 """

# fs可以填其中一个或几个 text_pronouns, text_teaser, mmr, text_rank, lead3, lda, lsi, nmf
res_score = text_summarize(doc, fs=[text_pronouns, text_teaser, mmr, text_rank, lead3, lda, lsi, nmf])
for rs in res_score:
    print(rs)


# feature_base
from nlg_yongzhuo import word_significance
from nlg_yongzhuo import text_pronouns
from nlg_yongzhuo import text_teaser
from nlg_yongzhuo import mmr
# graph_base
from nlg_yongzhuo import text_rank
# topic_base
from nlg_yongzhuo import lda
from nlg_yongzhuo import lsi
from nlg_yongzhuo import nmf
# nous_base
from nlg_yongzhuo import lead3


docs ="和投票目标的等级来决定新的等级.简单的说。" \
          "是上世纪90年代末提出的一种计算网页权重的算法! " \
          "当时，互联网技术突飞猛进，各种网页网站爆炸式增长。" \
          "业界急需一种相对比较准确的网页重要性计算方法。" \
          "是人们能够从海量互联网世界中找出自己需要的信息。" \
          "百度百科如是介绍他的思想:PageRank通过网络浩瀚的超链接关系来确定一个页面的等级。" \
          "Google把从A页面到B页面的链接解释为A页面给B页面投票。" \
          "Google根据投票来源甚至来源的来源，即链接到A页面的页面。" \
          "一个高等级的页面可以使其他低等级页面的等级提升。" \
          "具体说来就是，PageRank有两个基本思想，也可以说是假设。" \
          "即数量假设：一个网页被越多的其他页面链接，就越重）。" \
          "质量假设：一个网页越是被高质量的网页链接，就越重要。" \
          "总的来说就是一句话，从全局角度考虑，获取重要的信。"
# 1. word_significance
sums_word_significance = word_significance.summarize(docs, num=6)
print("word_significance:")
for sum_ in sums_word_significance:
    print(sum_)

# 2. text_pronouns
sums_text_pronouns = text_pronouns.summarize(docs, num=6)
print("text_pronouns:")
for sum_ in sums_text_pronouns:
    print(sum_)

# 3. text_teaser
sums_text_teaser = text_teaser.summarize(docs, num=6)
print("text_teaser:")
for sum_ in sums_text_teaser:
    print(sum_)
# 4. mmr
sums_mmr = mmr.summarize(docs, num=6)
print("mmr:")
for sum_ in sums_mmr:
    print(sum_)
# 5.text_rank
sums_text_rank = text_rank.summarize(docs, num=6)
print("text_rank:")
for sum_ in sums_text_rank:
    print(sum_)
# 6. lda
sums_lda = lda.summarize(docs, num=6)
print("lda:")
for sum_ in sums_lda:
    print(sum_)
# 7. lsi
sums_lsi = lsi.summarize(docs, num=6)
print("mmr:")
for sum_ in sums_lsi:
    print(sum_)
# 8. nmf
sums_nmf = nmf.summarize(docs, num=6)
print("nmf:")
for sum_ in sums_nmf:
    print(sum_)
# 9. lead3
sums_lead3 = lead3.summarize(docs, num=6)
print("lead3:")
for sum_ in sums_lead3:
    print(sum_)
