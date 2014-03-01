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
        self.daemon = True #如果设置此参数，则为后台线程
            
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
    初始化两个文件夹，比较是否一致
    '''
    def init_compare(self,new_my_dir):
        other_dir = {}
        for dir_name in GlobalVariable.dir_tree:
            if not dir_name == self.dir:
                other_dir[dir_name] = GlobalVariable.dir_tree[dir_name]
        #把自己和其它dir进行比较
        for file in new_my_dir:
            for other_dir_name in other_dir:
                #目标文件夹里没有此文件，新增
                if not other_dir[other_dir_name].has_key(file):
                    GlobalVariable.task_queue.put( Task(self.dir+file,other_dir_name+file,"add") )
                    continue
                
                #确实被更新过，并且md5不相同的
                if new_my_dir[ file ]['mtime'] > other_dir[other_dir_name][file]['mtime']:
                    if md5(self.dir+file) != md5(other_dir_name+file):
                        GlobalVariable.task_queue.put( Task(self.dir+file,other_dir_name+file,"modify") )
                        continue;
    
    def compare(self,new_my_dir,old_my_dir):
        ##除本dir之外的其它dir的状态
        other_dir = {}
        for dir_name in GlobalVariable.dir_tree:
            if not dir_name == self.dir:
                other_dir[dir_name] = GlobalVariable.dir_tree[dir_name]
        
        #上一次状态里没有，现在有了的。即为新增的
        for file in new_my_dir:
            if  not old_my_dir.has_key(file):
                for other_dir_name in other_dir:
                    GlobalVariable.task_queue.put( Task(self.dir+file,other_dir_name+file,"add") )
                    
        #上一次状态里有，现在没有了的。即为删除的
        for file in old_my_dir:
            if  not new_my_dir.has_key(file):
                 for other_dir_name in other_dir:
                    GlobalVariable.task_queue.put( Task(self.dir+file,other_dir_name+file,"delete") )
        
        #如果内容被更新了
        for file in new_my_dir:
            for other_dir_name in other_dir:
                #目标文件夹里没有此文件,或上一次状态里没有，跳过。
                #即，我有的，另外文件夹没有。可能是另外文件夹删除了，或我新增的。
                if not other_dir[other_dir_name].has_key(file) or not old_my_dir.has_key(file):
                    continue
                
                #确实被更新过，并且md5不相同的。
                #更新时间大于上次时间且大于另外一个文件夹时间
                if new_my_dir[ file ]['mtime'] > old_my_dir[file]['mtime'] and new_my_dir[ file ]['mtime'] > other_dir[other_dir_name][file]['mtime']:
                    if md5(self.dir+file) != md5(other_dir_name+file):
                        GlobalVariable.task_queue.put( Task(self.dir+file,other_dir_name+file,"modify") )
                        continue;