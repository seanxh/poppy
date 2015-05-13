#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os
import hashlib

def md5(file):
    if not os.path.isfile(file):
        return None
    hash_new = hashlib.sha1() #��hashlib.md5()  
    with open(file,'rb') as fp: #���ļ���һ��Ҫ�Զ����ƴ�  
        while True:  
            data = fp.read(1024) #��ȡ�ļ���  
            if not data: #ֱ�������ļ�  
                break  
            hash_new.update(data)  
        hash_value = hash_new.hexdigest() #���40λ(sha1)��32λ(md5)��ʮ������ַ�  
        fp.close()
    return hash_value  
    
def mkdir_p(target_file):
    if not os.path.isdir( os.path.dirname(target_file) ):
        mkdir_p( os.path.dirname(target_file) )
    if( os.path.isdir( target_file ) or os.path.isfile(target_file) ):
        return
    os.mkdir(target_file)