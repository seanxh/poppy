#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
import logging
from watchdog.observers import Observer
from handler import Handler
import time

class Watcher(threading.Thread):
    def __init__(self,dir,exclude,include):
        threading.Thread.__init__(self)
        self.dir = dir
        self.setDaemon(True)
        self.exclude = exclude
        self.include = include

        self.flag = True #是否需要运行的标识位
         
    def run(self):
        logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

        # event_handler = LoggingEventHandler()
        observer = Observer()
        event_handler = Handler(self.dir,self.exclude,self.include)
        observer.schedule(event_handler, path=self.dir, recursive=True)
        observer.start()
        try:
            while self.flag:
                time.sleep(0.5)
            observer.stop()
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
        
    def stop(self):
        self.flag = False