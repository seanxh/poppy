#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Queue
import threading

class GlobalVariable(object):
    #�ļ�״̬д����
    locks = {}
    #�ļ�״̬ӳ���
    dir_tree = {}
    #�������
    task_queue = Queue.Queue()
    #��ʼ�����д洢
    tmp_init_task_queue =  Queue.Queue()
    queue_lock = threading.Lock()
    #init flag����ʼ���ɹ����
    init = False
    
    def __init__(self):
        pass