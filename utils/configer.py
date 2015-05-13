#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'sean'

import ConfigParser

def parse_ini_2_dict(file):
    configs = {}

    list_option = ['include','exclude','strict']

    config = ConfigParser.ConfigParser()
    with open(file,"rw") as cfgfile:
        config.readfp(cfgfile)
        for k in config.sections():
            dict_conf = {'number':k}
            for c in config.items(k):
                if c[0] in list_option:
                    if c[1] == '':
                        dict_conf[c[0]] = []
                    else:
                        dict_conf[c[0]] = c[1].split(',')
                else:
                    dict_conf[c[0]] = c[1]

            configs[k] = dict_conf

    return configs

def write_dict_2_ini(file,configs):
    config = ConfigParser.ConfigParser()
    with open(file,"w") as cfgfile:
        i = 0
        for conf in configs:
            i+=1
            section  = str(conf['number'])
            del conf['number']
            config.add_section(section)

            for (key,value) in conf.iteritems():
                if type(value) is list:
                    config.set(section,str(key),','.join(value) )
                else:
                    config.set(section,str(key),value )
        config.write(cfgfile)