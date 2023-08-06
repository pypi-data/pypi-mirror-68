# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2019/11/11 20:44
# @author  : Mo
# @function:


from sklearn.decomposition import NMF
import numpy as np

arrary_org = np.array([[1, 3, 5, 7, 9],
                       [2, 4, 6, 8, 10],
                       [1, 4, 7, 11, 18],
                       [3, 4, 5, 10, 11],
                       [6, 1, 3, 2, 4]])

nmf_tfidf = NMF(n_components=3, max_iter=320)
res_nmf_w = nmf_tfidf.fit_transform(arrary_org)  # 基矩阵 or 权重矩阵
res_nmf_h = nmf_tfidf.components_  # 系数矩阵 or 降维矩阵
print(res_nmf_w)
print(res_nmf_h)