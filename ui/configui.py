#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'sean'

import index as indexUi
from Tkinter import  *
from utils import *
from functools import partial

class configUi(object):

    def __init__(self,conf_file,indexUI):

        self.top = Tk()
        self.top.title('Poppy--配置管理')

        self.indexUI = indexUI
        self.conf_file = conf_file
        self.original_configs  = parse_ini_2_dict(self.conf_file)

        self.width =  800
        self.height = 95+len(self.original_configs)*35

        self.widths = [8,5,18,18,18,18,18]

        self.top.geometry("%dx%d+%d+%d"%(self.width,self.height,int((self.top.winfo_screenwidth()-self.width)/2), int((self.top.winfo_screenheight()-self.height)/2)))

        title = PanedWindow(self.top,width=self.width)
        title.pack(fill=X)

        dele= Label(title, text="删除",width=self.widths[0])
        title.add(dele)

        lables = ["编号","源目录","目标目录","强制同步","排除","包含"]
        i=1
        for label in lables:
            l  = Label(title, text=label,width=self.widths[i])
            title.add(l)
            i+=1

        self.inputs = {}
        self.deletes = {}
        self.loadconfig()

        self.bfm = Frame(self.top)
        self.save = Button(self.bfm,text='Save',command=self.save,activeforeground='white',activebackground='blue')
        self.quit =  Button(self.bfm,text='Back',command=self.back,activeforeground='white',activebackground='red')
        self.new =  Button(self.bfm,text='New Line',command=self.newline,activeforeground='white',activebackground='red')
        self.new.pack(side=LEFT)
        self.save.pack(side=LEFT)
        self.quit.pack(side=LEFT)
        self.bfm.pack(side=BOTTOM)

        self.top.grab_set()
        # self.indexUI.grab_release()
        self.top.protocol("WM_DELETE_WINDOW", self.back)

    def loadconfig(self):
        enter_names = ['number','source','target','strict','exclude','include']

        m = 0
        for (k,config) in self.original_configs.iteritems():
            input = []
            m1 = PanedWindow(self.top,width=self.width)
            m1.pack(fill=X)

            number = config['number']
            # m+=1
            delete= Button(m1,text='Delete',command=partial(self.deleteone,number),activeforeground='white',activebackground='blue')
            m1.add(delete)
            self.deletes[number] = delete
            i=1
            for name in enter_names:
                value  = config[name] if config.has_key(name) else ''
                if type(value) is list:
                    value = ','.join(value)

                # default_value = StringVar()
                # default_value.set(value)
                # print value
                l = Entry(m1,width=self.widths[i])
                l.insert(0, value)
                l.pack()
                m1.add(l)
                input.append(l)
                i+=1

            self.inputs[config['number']] = input



    def newline(self):
        if len(self.inputs) >= 10:
            return

        m1 = PanedWindow(self.top,width=self.width)
        m1.pack(fill=X)
        input = []
        number = str(len(self.inputs)+1)

        # m+=1
        delete= Button(m1,text='Delete',command=partial(self.deleteone,number),activeforeground='white',activebackground='blue')
        m1.add(delete)
        self.deletes[number] = delete

        for k in range(1,7):
            default_value = StringVar()
            if k == 0:
                default_value.set(number)

            l = Entry(self.top,width=self.widths[k],textvariable=default_value)
            m1.add(l)
            input.append(l)

        self.inputs[number] = input

    def deleteone(self,number):
        print number
        if self.inputs.has_key(number):
            labels = self.inputs[number]
            for k in labels:
                k.destroy()
            del self.inputs[number]

            self.deletes[number].destroy()
            del self.deletes[number]


    def save(self):
        entry_names = ['number','source','target','strict','exclude','include']

        configs = {}
        for (k,v) in self.inputs.iteritems():
            conf = {}
            i=0
            key = ''
            for entry in v:
                if i == 0:
                    key = entry.get()
                conf[entry_names[i]] = entry.get()
                i+=1

            configs[key] = conf


        configs= sorted(configs.iteritems(), key=lambda d:d)

        conf =[c[1] for c in configs]

        write_dict_2_ini(self.conf_file,conf)

    def back(self):
        # index = indexUi.Index(self.conf_file)
        self.top.destroy()
        self.indexUI.normal()