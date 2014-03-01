#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
from GlobalVariable import GlobalVariable
from file import Files
from util import *
import time


class StatsThread(threading.Thread):
    def __init__(self,dir,patterns=[]):
        threading.Thread.__init__(self)
        self.daemon = True #������ô˲�������Ϊ��̨�߳�
        self.dir = dir #ά����DIR
        self.flag = True #�Ƿ���Ҫ���еı�ʶλ
        self.patterns = patterns
        self.obj_file = Files()
        GlobalVariable.dir_tree[self.dir] = self.obj_file.tree(self.dir,patterns)
        print self.dir+" init done"
        
    def stop(self):
        self.flag = False
        
    def run(self):
        while self.flag:
            file_list  = self.obj_file.tree(self.dir,self.patterns)
            if (file_list == False) or (len(file_list)==0) :
                time.sleep(5)
            else:
                GlobalVariable.locks[self.dir].acquire()
                GlobalVariable.dir_tree[self.dir] = file_list
                GlobalVariable.locks[self.dir].release()
                time.sleep(0.1)
            
            #sleep  1ms
            #print "Done"+self.dir
            
            
            #for f in GlobalVariable.dir_tree[self.dir]: 
            #    print  str(f)+":"+str(GlobalVariable.dir_tree[self.dir][f])
            