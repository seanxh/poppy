#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Queue
import threading

class GlobalVariable(object):
    #�ļ�״̬д����
    locks = {}
    #�ļ�״̬ӳ���
    dir_tree = {}
    dirs = []
    #�������
    task_queue = Queue.Queue()
    #��ʼ�����д洢
    tmp_init_task_queue =  Queue.Queue()
    queue_lock = threading.Lock()
    #�ƶ����ļ������moved��modify�����¼�,moveʱ��dest_path��¼��dict�У���modify�����δ��ļ�
    moved_dict = {}
    #init flag����ʼ���ɹ����
    init = False
    
    def __init__(self):
        pass