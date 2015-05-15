#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)   
sys.setdefaultencoding('gbk')

import os,time,shutil,hashlib,datetime
from utils.globalval import GlobalVariable
from utils.tools import *

class Task(object):
    def __init__(self,id,source_file,target_file,action):
        self.source_file = source_file
        self.target_file = target_file
        self.id = id
        self.action = action
        
    def __str__(self):
        target_file = self.target_file;source_file=self.source_file;
        
        if len(self.target_file) > 100:
            target_file = ''.join((self.target_file[0:15],'...',self.target_file[len(self.target_file)-30:]))
            
        if len(self.source_file) > 100:
            source_file = ''.join((self.source_file[0:15],'...',self.source_file[len(self.source_file)-30:]))
        # return str(self.action)+":" + " "*(7-len(self.action)) + "from " + str(source_file) + "\n"+" "*8+"To   " + str(target_file)

        return str(self.action) + " "*(7-len(self.action)) +":" + os.path.basename(source_file) +" "*2+"To  " + str(target_file) + ' TaskID:(' + str(self.id)+')'
        
    def do_it(self,console):
        actions = {
           "add": self.add,
           "delete": self.delete,
           "modify": self.modify,
           "move": self.move,
        }
        
        # console.write('------------------------------------\n')
        try:
            # console.write(str(self)+'\n')
            actions[self.action](console)
        except Exception,e:
            console.write(str(e)+'\n')
        # console.write('------------------------------------\n')
            
    def add(self,console):
        flag = False
        if not GlobalVariable.init:
            flag = False
        elif os.path.isfile( self.target_file ) or not os.path.isfile( self.source_file ):
            flag = True
        else:
            mkdir_p( os.path.dirname( self.target_file) )
            shutil.copyfile(self.source_file,self.target_file)
            # console.write('--------\n')
            # console.write('Done   ')
            # console.write(time.strftime('%m/%d %H:%M:%S',time.localtime()) + '\n')
            flag = True
        if flag :
             console.write('%s Success %s\n' % (str(self),time.strftime('%m/%d %H:%M:%S',time.localtime())))
        else:
             console.write('%s Failed %s\n' % (str(self),time.strftime('%m/%d %H:%M:%S',time.localtime())))
        return flag

    def modify(self,console):
        flag = False
        if not GlobalVariable.init:
            flag = False
        elif not os.path.isfile( self.source_file ):
            flag = True
        else:
            shutil.copyfile(self.source_file,self.target_file)
            # console.write('--------\n')
            # console.write('Done   ')
            # console.write(time.strftime('%m/%d %H:%M:%S',time.localtime()) + '\n')
            flag = True
        if flag :
             console.write('%s Success %s\n' % (str(self),time.strftime('%m/%d %H:%M:%S',time.localtime())))
        else:
             console.write('%s Failed %s\n' % (str(self),time.strftime('%m/%d %H:%M:%S',time.localtime())))
        return flag
        
    def delete(self,console):
        flag = False
        if not GlobalVariable.init:
            flag = False
        elif os.path.isfile( self.target_file ):
            os.remove( self.target_file )
            flag = True
        elif os.path.isdir( self.target_file ):
            os.rmdir( self.target_file )
            flag = True
        else:
            flag = True

        if flag :
             console.write('%s Success %s\n' % (str(self),time.strftime('%m/%d %H:%M:%S',time.localtime())))
        else:
             console.write('%s Failed %s\n' % (str(self),time.strftime('%m/%d %H:%M:%S',time.localtime())))
        return flag
        
    def move(self,console):
        flag = False
        if not GlobalVariable.init:
            flag = False
        elif os.path.isfile( self.source_file ) :
            shutil.move( self.source_file,self.target_file )
            flag = True
            # console.write('--------\n')
            # console.write('Done   ')
            # console.write(time.strftime('%m/%d %H:%M:%S',time.localtime()) + '\n')
        if flag :
             console.write('%s Success %s\n' % (str(self),time.strftime('%m/%d %H:%M:%S',time.localtime())))
        else:
             console.write('%s Failed %s\n' % (str(self),time.strftime('%m/%d %H:%M:%S',time.localtime())))
        return flag