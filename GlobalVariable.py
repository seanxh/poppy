#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Queue
import threading

class GlobalVariable(object):
    #文件状态写入锁
    locks = {}
    #文件状态映射表
    dir_tree = {}
    #任务队列
    task_queue = Queue.Queue()
    #初始化队列存储
    tmp_init_task_queue =  Queue.Queue()
    queue_lock = threading.Lock()
    #init flag，初始化成功与否
    init = False
    
    def __init__(self):
        pass