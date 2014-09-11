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
    def __init__(self,dir,patterns,watch=True):
        threading.Thread.__init__(self)
        self.dir = dir
        self.daemon = True #如果设置此参数，则为后台线程
        self.patterns = patterns
        self.watch = watch
        
        self.flag = True #是否需要运行的标识位
         
    def run(self):
        
        if not self.watch:
            return
        
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