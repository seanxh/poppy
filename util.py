#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os
import hashlib

def md5(file):
    if not os.path.isfile(file):
        return None
    hash_new = hashlib.sha1() #或hashlib.md5()  
    with open(file,'rb') as fp: #打开文件，一定要以二进制打开  
        while True:  
            data = fp.read(1024) #读取文件块  
            if not data: #直到读完文件  
                break  
            hash_new.update(data)  
        hash_value = hash_new.hexdigest() #生成40位(sha1)或32位(md5)的十六进制字符串  
        fp.close()
    return hash_value  
    
def mkdir_p(target_file):
    if not os.path.isdir( os.path.dirname(target_file) ):
        mkdir_p( os.path.dirname(target_file) )
    if( os.path.isdir( target_file ) or os.path.isfile(target_file) ):
        return
    os.mkdir(target_file)