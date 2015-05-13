#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Queue
import threading

class GlobalVariable(object):
    #文件状态写入锁
    locks = {}
    #文件状态映射表
    dir_tree = {}
    dirs = []
    #任务队列
    task_queue = Queue.Queue()
    #初始化队列存储
    tmp_init_task_queue =  Queue.Queue()
    queue_lock = threading.Lock()
    #移动的文件会产生moved和modify两个事件,move时将dest_path记录到dict中，在modify中屏蔽此文件
    moved_dict = {}
    #init flag，初始化成功与否
    init = False
    
    def __init__(self):
        pass