#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys,time,shutil,hashlib,datetime
import threading
import signal
from GlobalVariable import GlobalVariable
from Task import Task
from CompareThread import CompareThread
from StatsThread import StatsThread
from Worker import Worker
import config 
def select_dir():
    #可以同步的文件夹列表
    DIRS = config.DIRS
    
    print "YOU CAN CHOOSE FROM THE NEXT LIST:"
    for i in range(0,len(DIRS)):
        if len(DIRS[i]) < 2:
            print "DIRS["+str(i)+"] doesnt has 2 elements"
            sys.exit()
        print str(i+1)+":"+" "*(2-(i+1)//10)+"from "+DIRS[i][0]
        print "    to   "+DIRS[i][1]

    try:
        dir_num = int(raw_input("ENTER THE NUM OF DIR'S (0 exit):\n"))
    except Exception,e:
        print "you should enter a number,I can't convert that you input into a number,Thank you"
        sys.exit()
    if dir_num==0 or dir_num > len(DIRS):
        print "the index outrage dir's index"
        sys.exit()
    
    DIR = DIRS[dir_num-1][0]
    DIR2 = DIRS[dir_num-1][1]
    if len(DIRS[dir_num-1]) > 2:
        Patterns = DIRS[dir_num-1][2]
    else:
        Patterns = []
    
    if not os.path.isdir(DIR) or not os.path.isdir(DIR2):
        sys.exit()
    return  DIR,DIR2,Patterns

def init_global_lock(*dirs):
    for dir in dirs:
        GlobalVariable.locks[dir] = threading.Lock()

if  __name__ == '__main__':
    
    (DIR,DIR2,Patterns) = select_dir()
    print Patterns
    init_global_lock(DIR,DIR2)
    
    
    #开始遍历两个DIR，并把他们的文件列表维护到GlobalVariable.dir_tree中
    st1  = StatsThread(DIR,Patterns)
    st1.start()
    st2 = StatsThread(DIR2,Patterns)
    st2.start()
    
    com1 = CompareThread(DIR)
    com2 = CompareThread(DIR2)
    
    if GlobalVariable.task_queue.qsize() > 0 :
        #print '####################################'
        work = Worker(True);work.start();work.join();
        #print '####################################'
        choice = raw_input("the dirs are different,enter yes to Synchro Dirs:\n")
        
        
        if choice == "yes":
            GlobalVariable.init = True
            while GlobalVariable.tmp_init_task_queue.qsize():
                #如果队列为空，此方法会阻塞
                item = GlobalVariable.tmp_init_task_queue.get()
                GlobalVariable.task_queue.put( item )
                GlobalVariable.tmp_init_task_queue.task_done()
                
        else:
            sys.exit(0)
    else:
        GlobalVariable.init = True
    
 
    com1.start()
    com2.start()
    

    work=Worker()
    work.start()
    
    print "All init job is done,Synchronizing"
    
    st1.join()