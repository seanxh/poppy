#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
 
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from GlobalVariable import GlobalVariable
from Task import Task
from util import *
import time,re,os
 
class Handler(FileSystemEventHandler):
    def __init__(self,dir,patterns):
        self.dir = dir
        self.patterns = patterns
        #target_dir=target_dir
    
    def check_pattern(self,src_path):
        file = os.path.basename(src_path)
        if (len(self.patterns) > 0) :
            for pattern in self.patterns:
                pat = re.compile('^'+str(pattern)+'$')
                if pat.match( file ) != None:
                    return True
            return False
        return True
    
    def push_file_process_queue(self,src_path,type):
        if self.check_pattern(src_path):
            if ( src_path.find('.svn') == 0 ):
                return 
            for target_dir in GlobalVariable.dirs:
                if not self.dir == target_dir:
                    
                    if type == 'add' and ( os.path.isdir( target_dir+src_path) or os.path.isfile(target_dir+src_path) ):
                        continue
                    if type == 'delete' and not os.path.isdir( target_dir+src_path) and not os.path.isfile(target_dir+src_path):
                        continue
                     
                    if type == 'modify' and ( md5(self.dir+src_path) == md5(target_dir+src_path) ):
                        continue
                    GlobalVariable.task_queue.put( Task(self.dir+src_path,target_dir+src_path,type) )

    
    def on_created(self,event):
        if event.is_directory:
            pass
        else :
            self.push_file_process_queue(event.src_path[len(self.dir):],"add")
         
    def on_deleted(self,event):
        if event.is_directory:
            pass
        else :
            self.push_file_process_queue(event.src_path[len(self.dir):],"delete")
 
    def on_modified(self,event):
         if event.is_directory:
            pass
         else :
            if GlobalVariable.moved_dict.has_key(event.src_path):
                del GlobalVariable.moved_dict[event.src_path]
            else :
                self.push_file_process_queue(event.src_path[len(self.dir):],"modify")
 
    def on_moved(self,event):
        # pass
        # print "move",event.src_path,event.dest_path
        if event.dest_path.find(self.dir) != 0:
            self.push_file_process_queue(event.src_path[len(self.dir):],"delete")
        else :
            
            if not self.check_pattern(event.src_path) and not self.check_pattern(event.dest_path):
                return
        
            for target_dir in GlobalVariable.dirs:
                if not self.dir == target_dir:
                    
                    #如果对方的目标文件存在，continue
                    if os.path.isfile(target_dir+event.dest_path[len(self.dir):]):
                        continue
                    
                    GlobalVariable.moved_dict[event.dest_path] = 1
                    #如果对方文件不存在源文件，直接add，否则move
                    if not os.path.isfile(target_dir+event.src_path[len(self.dir):]):
                        print target_dir+event.src_path[len(self.dir):]
                        GlobalVariable.task_queue.put( Task(self.dir+event.dest_path[len(self.dir):],target_dir+event.dest_path[len(self.dir):],"add") )
                    else:
                        GlobalVariable.task_queue.put( Task(target_dir+event.src_path[len(self.dir):],target_dir+event.dest_path[len(self.dir):],"move") )
 
 
if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='Z:/monitor/', recursive=True)
    observer.start()
 
    try:
        print "started myWatch"
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
