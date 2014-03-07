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
        self.daemon = True #如果设置此参数，则为后台线程
            
        self.new_my_dir = GlobalVariable.dir_tree[self.dir]
        GlobalVariable.locks[self.dir].acquire()
        self.init_compare(self.new_my_dir,self.target_dir)
        GlobalVariable.locks[self.dir].release()


            
    '''
    初始化两个文件夹，比较是否一致
    '''
    def init_compare(self,new_my_dir,target_dir):
        target_dir_tree = GlobalVariable.dir_tree[target_dir]
        #把自己和其它dir进行比较
        for file in new_my_dir:
                #目标文件夹里没有此文件，新增
                if not target_dir_tree.has_key(file):
                    GlobalVariable.task_queue.put( Task(self.dir+file,target_dir+file,"add") )
                    continue
                
                #确实被更新过，并且md5不相同的
                if new_my_dir[ file ]['mtime'] > target_dir_tree[file]['mtime']:
                    if md5(self.dir+file) != md5(target_dir+file):
                        GlobalVariable.task_queue.put( Task(self.dir+file,target_dir+file,"modify") )
                        continue;
    