#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys,time,shutil,hashlib,datetime
import threading
import signal
from GlobalVariable import GlobalVariable
from CompareThread import CompareThread
from StatsThread import StatsThread
from Worker import Worker
from Watcher import Watcher
import config 
def select_dir():
    #可以同步的文件夹列表
    DIRS = config.DIRS
    
    print "YOU CAN CHOOSE FROM THE NEXT LIST:"
    for i in range(0,len(DIRS)):
        if len(DIRS[i]) < 2:
            print "DIRS["+str(i)+"] doesnt has 2 elements"
            sys.exit()
        
        if type(DIRS[i][0]) is list:
            source_dir =  DIRS[i][0][0]
        else:
            source_dir =  DIRS[i][0]
        
        if type(DIRS[i][1]) is list:
            target_dir =  DIRS[i][1][0]
        else:
            target_dir =  DIRS[i][1]
        
        print str(i+1)+":"+" "*(2-(i+1)//10)+"from "+source_dir
        print "    to   "+target_dir

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

    if type(DIR) is str:
        DIR = [DIR,1]

    if type(DIR2) is str:
        DIR2 = [DIR2,1]
        
    if not type(DIR) is list:
        print 'DIR Config errr'
     
    if not type(DIR2) is list:
        print 'DIR2 Config errr'

    
    if os.sep == '\\':
        DIR[0] = DIR[0].replace('/','\\')
        DIR2[0] = DIR2[0].replace('/','\\')
    
    if len(DIRS[dir_num-1]) > 2:
        StrictDIR =  DIRS[dir_num-1][2]
        if  len(DIRS[dir_num-1]) == 4 :
            Patterns = DIRS[dir_num-1][3]
        else:
            Patterns = []
    else:
        Patterns = []
        StrictDIR = []
    
    if not os.path.isdir(DIR[0]) or not os.path.isdir(DIR2[0]):
        sys.exit()

    return  DIR,DIR2,Patterns,StrictDIR

def init_global_lock(*dirs):
    for dir in dirs:
        GlobalVariable.locks[dir] = threading.Lock()
        GlobalVariable.dirs.append( dir )

if  __name__ == '__main__':
    
    (DIR_config,DIR2_config,Patterns,StrictDIR) = select_dir()
    
    DIR = DIR_config[0]
    DIR2 = DIR2_config[0]
    
    init_global_lock(DIR,DIR2)
    
    #开始遍历两个DIR，并把他们的文件列表维护到GlobalVariable.dir_tree中
    statThread = []
    for dir in StrictDIR:
        init_global_lock( DIR+dir+os.sep,DIR2+dir+os.sep )
        st1 = StatsThread(DIR+dir+os.sep,Patterns)
        st1.start()
        statThread.append ( st1 )
        st2 = StatsThread(DIR2+dir+os.sep,Patterns)
        st2.start()
        statThread.append ( st2 )
    
    for dir in StrictDIR:
        CompareThread(DIR+dir+os.sep,DIR2+dir+os.sep)
        CompareThread(DIR2+dir+os.sep,DIR+dir+os.sep)        
    
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
    
    for st in statThread:
        st.stop()
    
    for st in statThread:
        st.join()
    
    GlobalVariable.locks = {}
    GlobalVariable.dirs = []
    init_global_lock(DIR,DIR2)
    
    work=Worker()
    print Patterns
    print DIR
    print DIR2
    watcher1 = Watcher(DIR,Patterns,DIR_config[1])
    watcher2 = Watcher(DIR2,Patterns,DIR2_config[1])
    
    watcher1.start()
    watcher2.start()
    
    GlobalVariable.init = True
    
    work.start()
    
    print "All init job is done,Synchronizing"
    
    watcher1.join()
    watcher2.join()
    work.join()