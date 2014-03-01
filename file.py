#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os,stat
import hashlib  
import time,re

class Files(object):
    def __init__(self):
        self._dir_tree = {}
        self.dir_name = ''
        self.missing = {}
        pass
    '''
    列出一个dir中的所有子文件
    @dir_name 绝对路径 /root/
    @return {'/root/test.txt':{'mtime':xx,'size':'xxx'},'/root/xxx':{...}}
    '''
    def tree(self,dir_name,patterns=[]):
        if not self.missing.has_key(dir_name):
            self.missing[dir_name] = False
        self._dir_tree = {}
        self.dir_name = dir_name
        #print dir_name
        if os.path.isdir(dir_name):
            if self.missing[dir_name] == True:
                print str(dir_name) + ' come back'
                self.missing[dir_name] = False
            #当遍历一个文件夹到一半时，断开网络，会返回空列表，导致删除文件
            if self._tree(dir_name,patterns) == False:
                return False
        else:
            print str(dir_name) + ' missed,please check'
            self.missing[dir_name] = True
            return False
        self.dir_name = ''
        return self._dir_tree
    
    def _tree(self,dir_name,patterns):
        try:
            dirinfo = os.listdir(dir_name)
            for file in dirinfo:
                if (len(patterns) > 0) and ( file.find('.') != -1):
                    flag = False
                    for pattern in patterns:
                        pat = re.compile('^'+str(pattern)+'$')
                        if pat.match( file ) != None:
                            flag = True
                            break
                    if not flag:
                        continue
                    
                statinfo = os.stat(dir_name+file)
                
                if stat.S_ISREG( statinfo[ stat.ST_MODE]): 
                    #statinfo = os.stat(dir_name+file)
                    #最后修改时间
                    self._dir_tree[(dir_name+file)[len(self.dir_name):]] = {'mtime':statinfo.st_mtime,'size':statinfo.st_size}
                elif stat.S_ISDIR( statinfo[ stat.ST_MODE]):
                    self._tree(dir_name+file+'/',patterns)
                #if os.path.isdir(dir_name+file): 
                
            return True
        except Exception,e:
            print e
            self._dir_tree = {}
            return False
        
if  __name__ == '__main__':
    log = open('D:/log.txt', 'a')
    log.write("%s\n" % ('dd') )
    log.close()
    sys.exit('s')
    DIR = r"D:/openplatform/protected/"
    file = Files()
    file_list  = file.tree(DIR)
    for f in file_list: 
        print  str(f)+":"+str(file_list[f])