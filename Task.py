#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)   
sys.setdefaultencoding('gbk')

import os,time,shutil,hashlib,datetime
from GlobalVariable import GlobalVariable
from util import *

class Task(object):
    def __init__(self,source_file,target_file,action):
        self.source_file = source_file
        self.target_file = target_file
        self.action = action
        
    def __str__(self):
        target_file = self.target_file;source_file=self.source_file;
        
        if len(self.target_file) > 50:
            target_file = ''.join((self.target_file[0:15],'...',self.target_file[len(self.target_file)-30:]))
            
        if len(self.source_file) > 50:
            source_file = ''.join((self.source_file[0:15],'...',self.source_file[len(self.source_file)-30:]))
        return str(self.action)+":" + " "*(7-len(self.action)) + "from " + str(source_file) + "\n"+" "*8+"To   " + str(target_file)
        
    def do_it(self):
        actions = {
           "add": self.add,
           "delete": self.delete,
           "modify": self.modify,
           "move": self.move,
        }
        
        print '------------------------------------'
        #执行
        try:
            print self
            actions[self.action]()
        except Exception,e:
            print e
        print '------------------------------------'
            
    def add(self):
        #如果要添加的文件已经存在，不执行添加操作
        #如果要添加的文件源已经不存在 ，不执行添加操作
        if os.path.isfile( self.target_file ) or not os.path.isfile( self.source_file ):
            return True
        if not GlobalVariable.init:
            return False
        mkdir_p( os.path.dirname( self.target_file) )
        shutil.copyfile(self.source_file,self.target_file)
        print '--------'
        print "Done   ",
        print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return True
        
    def modify(self):
        #如果source文件已经删除，就不要执行复制了
        #如果修改的文件已经不存在，不要执行修改了
        if not os.path.isfile( self.source_file ) or not os.path.isfile( self.target_file ):
            return True
        if not GlobalVariable.init:
            return False
        shutil.copyfile(self.source_file,self.target_file)  
        print '--------'
        print "Done   ",
        print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        #print datetime.datetime.now()
        return True
        
    def delete(self):
        if not GlobalVariable.init:
            return False
        if os.path.isfile( self.target_file ):
            os.remove( self.target_file )
        elif os.path.isdir( self.target_file ):
            os.rmdir( self.target_file )
        else:
            return True
        print '--------'
        print "Done   ",
        print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return True
        
    def move(self):
        if not GlobalVariable.init:
            return False
        if os.path.isfile( self.source_file ) :
            shutil.move( self.source_file,self.target_file )
            print '--------'
            print "Done   ",
            print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return True