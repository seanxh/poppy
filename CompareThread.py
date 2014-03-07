#!/usr/bin/env python
# -*- coding: utf-8 -*-
from GlobalVariable import GlobalVariable
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from file import Files
from Task import Task
from util import *
import time

class CompareThread():
    def __init__(self,dir,target_dir):
        self.dir = dir
        self.target_dir = target_dir
        self.daemon = True #������ô˲�������Ϊ��̨�߳�
            
        self.new_my_dir = GlobalVariable.dir_tree[self.dir]
        GlobalVariable.locks[self.dir].acquire()
        self.init_compare(self.new_my_dir,self.target_dir)
        GlobalVariable.locks[self.dir].release()


            
    '''
    ��ʼ�������ļ��У��Ƚ��Ƿ�һ��
    '''
    def init_compare(self,new_my_dir,target_dir):
        target_dir_tree = GlobalVariable.dir_tree[target_dir]
        #���Լ�������dir���бȽ�
        for file in new_my_dir:
                #Ŀ���ļ�����û�д��ļ�������
                if not target_dir_tree.has_key(file):
                    GlobalVariable.task_queue.put( Task(self.dir+file,target_dir+file,"add") )
                    continue
                
                #ȷʵ�����¹�������md5����ͬ��
                if new_my_dir[ file ]['mtime'] > target_dir_tree[file]['mtime']:
                    if md5(self.dir+file) != md5(target_dir+file):
                        GlobalVariable.task_queue.put( Task(self.dir+file,target_dir+file,"modify") )
                        continue;
    