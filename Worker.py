#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading,time
from GlobalVariable import GlobalVariable
from Task import Task

class Worker(threading.Thread):
    def __init__(self,once=False):
        threading.Thread.__init__(self)
        self.daemon = True #如果设置此参数，则为后台线程
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
            #如果队列为空，此方法会阻塞
            item = GlobalVariable.task_queue.get()
            #处理队列
            if not item.do_it():
                GlobalVariable.tmp_init_task_queue.put( item )

            GlobalVariable.task_queue.task_done()
            time.sleep(0.01)