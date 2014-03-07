#!/usr/bin/env python
# -*- coding: utf-8 -*-

##要同步的文件夹~
##每个ITEM包含要同步的两个文件夹的名字
##第三项为strict的dir名称，如果不为空在初始化时必须要求两个子文件夹完全相同
##第四项为文件名匹配表达式
DIRS = (
    [r"D:/openplatform/protected/",r"Z:/yii/protected/",["strict_dir"],['.*\.html']],
    [r"D:/yii/protected/",r"Z:/yii/protected/",[],['.*\.html']],
    [r"D:/yii/protected/modules/",r"Z:/yii/protected/modules/",[],['.*\.html']],
)