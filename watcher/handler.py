#!/usr/bin/python
# -*- coding: UTF-8 -*-
 
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from task.task import Task
from utils import *

import time,re,os
 
class Handler(FileSystemEventHandler):
    def __init__(self,dir,exclude,include):
        self.dir = dir
        self.exclude = exclude
        self.include = include
        #target_dir=target_dir
    
    def check_pattern(self,src_path):
        if src_path.find('.svn') == 0:
            return False
    
        file = os.path.basename(src_path)

        pat = re.compile('^.*\.svn.*$')
        if pat.match( file ) != None:
            return False

        if (len(self.exclude) > 0) :
            for pattern in self.exclude:
                pat = re.compile(str(pattern))
                if pat.search( src_path ) != None:##match exclude, Fail
                    return False

        if (len(self.include) > 0) :
            for pattern in self.include:
                pat = re.compile(str(pattern))
                if pat.search( src_path ) == None:#not match include ,Fail
                    return False

        return True
    
    def push_file_process_queue(self,src_path,type):
        if self.check_pattern(src_path):
            for target_dir in GlobalVariable.dirs:
                if not self.dir == target_dir:
                    #if type == 'add' and ( os.path.isdir( target_dir+src_path) or os.path.isfile(target_dir+src_path) ):
                    #    continue
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
                        # print target_dir+event.src_path[len(self.dir):]
                        GlobalVariable.task_queue.put( Task(self.dir+event.dest_path[len(self.dir):],target_dir+event.dest_path[len(self.dir):],"add") )
                    else:
                        GlobalVariable.task_queue.put( Task(target_dir+event.src_path[len(self.dir):],target_dir+event.dest_path[len(self.dir):],"move") )
