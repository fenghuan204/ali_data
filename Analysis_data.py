#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2015 windy zhao <187063598@qq.com>

"""

import sklearn
import numpy as np
import sys
import os
from pandas import Series, DataFrame
import pandas as pd

def openfile(data):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.abspath(os.path.join(current_dir,'data'))
    # print data_path
    sys.path.append(data_path)
    # all_data = np.load(os.path.join(data_path, 'tianchi_mobile_recommend_train_item.csv'))
    fi=open(os.path.join(data_path, data),'r')
    for line in fi.readlines():
         print line.strip('\n').split(',')

    fi.close()

    # d=pd.read_csv(os.path.join(data_path, data))
    # d=pd.read_csv('E:\github\data\tianchi_mobile_recommend_train_item.csv')
    # print os.path.join(data_path, 'tianchi_mobile_recommend_train_item.csv')
    # print d.head()



def main():
    # openfile('tianchi_mobile_recommend_train_item.csv')

    openfile('tianchi_mobile_recommend_train_user.csv')
if __name__ == '__main__':
    main()




