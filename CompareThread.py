#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
from GlobalVariable import GlobalVariable
from file import Files
from Task import Task
from util import *
import time

class CompareThread(threading.Thread):
    def __init__(self,dir):
        threading.Thread.__init__(self)
        self.dir = dir
        self.daemon = True #������ô˲�������Ϊ��̨�߳�
            
        self.new_my_dir = GlobalVariable.dir_tree[self.dir]
        self.old_my_dir = {}
        GlobalVariable.locks[self.dir].acquire()
        self.init_compare(self.new_my_dir)
        GlobalVariable.locks[self.dir].release()
        
    def run(self):
        
        while GlobalVariable.locks[self.dir].acquire():
            self.old_my_dir = self.new_my_dir
            self.new_my_dir = GlobalVariable.dir_tree[self.dir]
            self.compare(self.new_my_dir,self.old_my_dir)
            GlobalVariable.locks[self.dir].release()
            time.sleep(0.01)
            
    '''
    ��ʼ�������ļ��У��Ƚ��Ƿ�һ��
    '''
    def init_compare(self,new_my_dir):
        other_dir = {}
        for dir_name in GlobalVariable.dir_tree:
            if not dir_name == self.dir:
                other_dir[dir_name] = GlobalVariable.dir_tree[dir_name]
        #���Լ�������dir���бȽ�
        for file in new_my_dir:
            for other_dir_name in other_dir:
                #Ŀ���ļ�����û�д��ļ�������
                if not other_dir[other_dir_name].has_key(file):
                    GlobalVariable.task_queue.put( Task(self.dir+file,other_dir_name+file,"add") )
                    continue
                
                #ȷʵ�����¹�������md5����ͬ��
                if new_my_dir[ file ]['mtime'] > other_dir[other_dir_name][file]['mtime']:
                    if md5(self.dir+file) != md5(other_dir_name+file):
                        GlobalVariable.task_queue.put( Task(self.dir+file,other_dir_name+file,"modify") )
                        continue;
    
    def compare(self,new_my_dir,old_my_dir):
        ##����dir֮�������dir��״̬
        other_dir = {}
        for dir_name in GlobalVariable.dir_tree:
            if not dir_name == self.dir:
                other_dir[dir_name] = GlobalVariable.dir_tree[dir_name]
        
        #��һ��״̬��û�У��������˵ġ���Ϊ������
        for file in new_my_dir:
            if  not old_my_dir.has_key(file):
                for other_dir_name in other_dir:
                    GlobalVariable.task_queue.put( Task(self.dir+file,other_dir_name+file,"add") )
                    
        #��һ��״̬���У�����û���˵ġ���Ϊɾ����
        for file in old_my_dir:
            if  not new_my_dir.has_key(file):
                 for other_dir_name in other_dir:
                    GlobalVariable.task_queue.put( Task(self.dir+file,other_dir_name+file,"delete") )
        
        #������ݱ�������
        for file in new_my_dir:
            for other_dir_name in other_dir:
                #Ŀ���ļ�����û�д��ļ�,����һ��״̬��û�У�������
                #�������еģ������ļ���û�С������������ļ���ɾ���ˣ����������ġ�
                if not other_dir[other_dir_name].has_key(file) or not old_my_dir.has_key(file):
                    continue
                
                #ȷʵ�����¹�������md5����ͬ�ġ�
                #����ʱ������ϴ�ʱ���Ҵ�������һ���ļ���ʱ��
                if new_my_dir[ file ]['mtime'] > old_my_dir[file]['mtime'] and new_my_dir[ file ]['mtime'] > other_dir[other_dir_name][file]['mtime']:
                    if md5(self.dir+file) != md5(other_dir_name+file):
                        GlobalVariable.task_queue.put( Task(self.dir+file,other_dir_name+file,"modify") )
                        continue;