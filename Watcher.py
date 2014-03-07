#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
from GlobalVariable import GlobalVariable
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from Task import Task
from util import *
from Handler import Handler
import time

class Watcher(threading.Thread):
    def __init__(self,dir,patterns):
        threading.Thread.__init__(self)
        self.dir = dir
        self.daemon = True #������ô˲�������Ϊ��̨�߳�
        self.patterns = patterns
        
        self.flag = True #�Ƿ���Ҫ���еı�ʶλ
         
    def run(self):
        
        event_handler = Handler(self.dir,self.patterns)
        observer = Observer()
        observer.schedule(event_handler, path=self.dir, recursive=True)
        observer.start()
        try:
            while self.flag:
                time.sleep(0.5)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
        
    def stop(self):
        self.flag = False