#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2015 windy zhao <187063598@qq.com>

"""

import pandas as pd
import statsmodels.api as sm
from sklearn import linear_model
import numpy as np
import sys
import os
from pandas import Series, DataFrame

# train = pd.read_csv("recommend_train_user_slice.csv")
train = pd.read_csv("demo.csv")
# train = pd.read_csv("test.csv")
train_cols = train.columns[0:1]
DataFrame(train, columns=['click','sc'])
# print [train['click'],train['cf']]
clf = linear_model.LinearRegression()
input=DataFrame(train, columns=['click','sc'])
clf.fit(train[train_cols] ,train['buy'])
# The coefficients
print clf
print('Coefficients: \n', clf.coef_)
# The mean square error
print("Residual sum of squares: %.2f"
      % np.mean((clf.predict(train[train_cols]) - train['buy']) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % clf.score(train[train_cols], train['buy']))#



logit = sm.Logit(train['buy'], train[train_cols])
# logit = sm.Logit(train['buy'], input)
result = logit.fit()
print result.summary()
print result.conf_int()

# combos = pd.read_csv("vectors.csv")
# train_cols = combos.columns[2:]
# combos['prediction'] = result.predict(combos[train_cols])
#
# predicts = defaultdict(set)
#
# print train.head()

