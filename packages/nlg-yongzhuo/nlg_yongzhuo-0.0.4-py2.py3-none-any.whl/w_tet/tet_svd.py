# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2019/11/12 10:39
# @author  : Mo
# @function:


# ①读取图片
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

img_eg = mpimg.imread("../img/beauty.jpg")
print(img_eg.shape)
# 图片的大小是600×400×3

# ②奇异值分解

img_temp = img_eg.reshape(600, 400 * 3)
U,Sigma,VT = np.linalg.svd(img_temp)
# 我们先将图片变成600×1200，再做奇异值分解。从svd函数中得到的奇异值sigma它是从大到小排列的。

# ③取前部分奇异值重构图片

# 取前60个奇异值
sval_nums = 60
img_restruct1 = (U[:,0:sval_nums]).dot(np.diag(Sigma[0:sval_nums])).dot(VT[0:sval_nums,:])
img_restruct1 = img_restruct1.reshape(600,400,3)

# 取前120个奇异值
sval_nums = 120
img_restruct2 = (U[:,0:sval_nums]).dot(np.diag(Sigma[0:sval_nums])).dot(VT[0:sval_nums,:])
img_restruct2 = img_restruct2.reshape(600,400,3)
# 将图片显示出来看一下，对比下效果

fig, ax = plt.subplots(1,3,figsize = (24,32))

ax[0].imshow(img_eg)
ax[0].set(title = "src")
ax[1].imshow(img_restruct1.astype(np.uint8))
ax[1].set(title = "nums of sigma = 60")
ax[2].imshow(img_restruct2.astype(np.uint8))
ax[2].set(title = "nums of sigma = 120")