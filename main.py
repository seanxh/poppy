#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys,time,shutil,hashlib,datetime
import threading
from utils import *
from watcher import *
from task import *
import logging
import config

def select_dir():
    #可以同步的文件夹列表
    # DIRS = config.DIRS
    DIRS = parse_ini_2_dict( os.path.dirname( os.path.abspath(__file__) ) + '/config/config.ini' )

    print "YOU CAN CHOOSE FROM THE NEXT LIST:"
    for (i,conf) in DIRS.iteritems():

        DIRS[i]['source'] = source_dir = conf['source'] if conf.has_key('source') else ''
        DIRS[i]['target'] = target_dir = conf['target'] if conf.has_key('target') else ''
        DIRS[i]['strict'] = strict_dir = conf['strict'] if conf.has_key('strict') and type(conf['strict']) is list else []
        DIRS[i]['exclude'] = exclude = conf['exclude'] if conf.has_key('exclude') and type(conf['exclude']) is list else []
        DIRS[i]['include'] = include = conf['include'] if conf.has_key('include') and type(conf['include']) is list else []


        if len(source_dir) <= 0:
            continue
        if len(target_dir) <= 0 :
            continue

        print i+":"+" "*(2-(len(i)+1)//10)+"from "+source_dir
        print "    to   "+target_dir

    try:
        dir_num = raw_input("ENTER THE NUM OF DIR'S (0 exit):\n")
    except Exception,e:
        print "you should enter a number,I can't convert that you input into a number,Thank you"
        sys.exit()

    if not DIRS.has_key(dir_num):
        print "the index outrage dir's index"
        sys.exit()


    source_dir = DIRS[dir_num]['source']
    target_dir = DIRS[dir_num]['target']
    StrictDIR = DIRS[dir_num]['strict']
    excludeDIR = DIRS[dir_num]['exclude']
    includeDIR = DIRS[dir_num]['include']

    
    if os.sep == '\\':
        source_dir = source_dir.replace('/','\\')
        target_dir = target_dir.replace('/','\\')

    if not os.path.isdir(source_dir) :
        print "the dir %s is not exit" %(source_dir)
        sys.exit()
    elif not os.path.isdir(target_dir):
        print "the dir %s is not exit" %(target_dir)
        sys.exit()

    return  source_dir,target_dir,StrictDIR,excludeDIR,includeDIR

def init_global_lock(*dirs):
    for dir in dirs:
        GlobalVariable.locks[dir] = threading.Lock()
        GlobalVariable.dirs.append( dir )

if  __name__ == '__main__':

    (source_dir,target_dir,strictDIR,excludeDIR,includeDIR) = select_dir()

    # init_global_lock(source_dir,target_dir)
    
    #开始遍历两个DIR，并把他们的文件列表维护到GlobalVariable.dir_tree中
    # statThread = []
    # for dir in strictDIR:
    #     init_global_lock( source_dir+dir+os.sep,target_dir+dir+os.sep )
    #     st1 = StatsThread(source_dir+dir+os.sep,patterns)
    #     st1.start()
    #     statThread.append ( st1 )
    #     st2 = StatsThread(target_dir+dir+os.sep,patterns)
    #     st2.start()
    #     statThread.append ( st2 )
    #
    # for dir in strictDIR:
    #     CompareThread(source_dir+dir+os.sep,target_dir+dir+os.sep)
    #     CompareThread(target_dir+dir+os.sep,source_dir+dir+os.sep)
    #
    # if GlobalVariable.task_queue.qsize() > 0 :
    #     #print '####################################'
    #     work = Worker(True);work.start();work.join();
    #     #print '####################################'
    #     choice = raw_input("the dirs are different,enter yes to Synchro Dirs:\n")
    #
    #
    #     if choice == "yes":
    #         GlobalVariable.init = True
    #         while GlobalVariable.tmp_init_task_queue.qsize():
    #             #如果队列为空，此方法会阻塞
    #             item = GlobalVariable.tmp_init_task_queue.get()
    #             GlobalVariable.task_queue.put( item )
    #             GlobalVariable.tmp_init_task_queue.task_done()
    #
    #     else:
    #         sys.exit(0)
    # else:
    #     GlobalVariable.init = True
    #
    # for st in statThread:
    #     st.stop()
    #
    # for st in statThread:
    #     st.join()


    KillKeyboard()

    main = Main(source_dir,target_dir,strictDIR,excludeDIR,includeDIR,sys.stderr)

    main.start()

    while True:
        time.sleep(1)


    #
    # GlobalVariable.locks = {}
    # GlobalVariable.dirs = []
    # init_global_lock(source_dir,target_dir)
    #
    # work=Worker()
    #
    # KillKeyboard()
    #
    #
    # watcher1 = Watcher(source_dir,patterns)
    # # watcher2 = Watcher(target_dir,Patterns,0)
    #
    # watcher1.start()
    #
    # GlobalVariable.init = True
    #
    # work.start()
    #
    # print "All init job is done,Synchronizing"
    #
    # watcher1.join()
    # work.join()