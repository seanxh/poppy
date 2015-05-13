#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading,time
from utils.globalval import GlobalVariable
import Queue
import sys

class Worker(threading.Thread):
    def __init__(self,console=sys.stderr,once=False):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.flag = True
        self.once = once
        self.console = console
        
    def stop(self):
        self.flag = False
        
    def condition(self):
        if self.once :
            return GlobalVariable.task_queue.qsize()
        else:
            return self.flag
            
    def run(self):

        while self.condition():
            try:
                item = GlobalVariable.task_queue.get(block=False)
                if not item.do_it(self.console):
                    GlobalVariable.tmp_init_task_queue.put( item )

                GlobalVariable.task_queue.task_done()
            except Queue.Empty,e:
                time.sleep(0.01)
            except RuntimeError,e:
                print e.args
