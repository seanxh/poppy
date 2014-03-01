#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading,time
from GlobalVariable import GlobalVariable
from Task import Task

class Worker(threading.Thread):
    def __init__(self,once=False):
        threading.Thread.__init__(self)
        self.daemon = True #������ô˲�������Ϊ��̨�߳�
        self.flag = True
        self.once = once
        
    def stop(self):
        self.flag = False
        
    def condition(self):
        if self.once :
            return GlobalVariable.task_queue.qsize()
        else:
            return self.flag
            
    def run(self):
        
        while self.condition():
            #�������Ϊ�գ��˷���������
            item = GlobalVariable.task_queue.get()
            #�������
            if not item.do_it():
                GlobalVariable.tmp_init_task_queue.put( item )

            GlobalVariable.task_queue.task_done()
            time.sleep(0.01)