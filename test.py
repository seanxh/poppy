#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
# author : firefoxbug
# E-Mail : wanghuafire@gmail.com
# Blog   : www.firefoxbug.net
 
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os,sys
 
 
class MyHandler(FileSystemEventHandler):
    def on_created(self,event):
        if event.is_directory:
            print event.event_type,event.src_path
        else :
            print event.event_type,event.src_path
         
    def on_deleted(self,event):
        if event.is_directory:
            print event.event_type,event.src_path
        else :
            print event.event_type,event.src_path
 
    def on_modified(self,event):
        if not event.is_directory:
            print event.event_type,event.src_path
 
    def on_moved(self,event):
        print "move",event.src_path,event.dest_path
 
 
if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='D:/rms_249-4/protected/modules/', recursive=True)
    observer.start()
 
    try:
        print "started myWatch"
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
