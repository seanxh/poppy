#!/usr/bin/python
# -*- coding: UTF-8 -*-

__author__ = 'sean'
import configui as configUi
from Tkinter import  *
from utils import *
from watcher import *

class Index(object):
    def __init__(self,conf_file):

        self.top = Tk()
        self.top.title('Poppy--文件夹同步')
        self.width =  500
        self.height = 200

        self.top.geometry("%dx%d+%d+%d"%(self.width,self.height,int((self.top.winfo_screenwidth()-self.width)/2), int((self.top.winfo_screenheight()-self.height)/2)))


        self.bfm = Frame(self.top)


        self.conf_file = conf_file

        self.original_configs  = parse_ini_2_dict(self.conf_file)
        self.configs_str = self.parse_config_2_str(self.original_configs)
        self.option_variable = StringVar(self.top)
        self.option_variable.set(self.configs_str[0]) # default value
        # w = apply(OptionMenu, (self.top, variable) + tuple(self.configs_str))
        self.option = OptionMenu(self.bfm, self.option_variable,*self.configs_str)
        self.option.config(width=50)
        self.option.pack(side=LEFT)


        self.start = Button(self.bfm,text='Start',command=self.run,activeforeground='white',activebackground='blue')
        self.config =  Button(self.bfm,text='目录管理',command=self.configui,activeforeground='white',activebackground='red')
        self.start.pack(side=LEFT)
        self.config.pack(side=LEFT)
        self.bfm.pack(side=TOP)

        sb = Scrollbar(self.top)
        sb.pack(side=RIGHT,fill=Y)

        self.text = Text(self.top,yscrollcommand=sb.set,bd=10)
        self.text.pack()
        self.text_sum = 0
        self.text.configure(state=DISABLED)
        self.main_thread =  None

    def init_optionMenu(self):
        self.original_configs  = parse_ini_2_dict(self.conf_file)
        self.configs_str = self.parse_config_2_str(self.original_configs)

        # self.option_variable = StringVar(self.top)
        # self.option_variable.set(self.configs_str[0]) # default value
        self.option['menu'].delete(0, 'end')
        for choice in self.configs_str:
            self.option['menu'].add_command(label=choice,command=lambda v=choice: self.option_variable.set(v))

    def run(self):
        if self.start.cget('text') == 'Start':
            selected_str = self.option_variable.get()
            section  = selected_str.split(':')[0].strip()
            if self.start_synchronize(self.original_configs[section]):
                self.start.config(text='Stop')
                self.option.config(state=DISABLED)
        else:
            self.start.config(text='Start')
            self.option.config(state=NORMAL)
            self.stop_synchronize()

    def start_synchronize(self,conf):
        self.text.configure(state=NORMAL)
        self.text.delete(0.0,END)
        self.text.configure(state=DISABLED)
        self.text_sum = 0

        self.main_thread = Main(conf['source'],conf['target'],conf['strict'],conf['exclude'],conf['include'],self)
        if not self.main_thread.start():
            self.main_thread = None
            return False
        return True



    def stop_synchronize(self):
        if self.main_thread is not None:
            self.main_thread.stop()
            self.main_thread = None

    def disable(self):
        self.start.config(state=DISABLED)
        self.config.config(state=DISABLED)

    def normal(self):
        self.init_optionMenu()
        self.start.config(state=NORMAL)
        self.config.config(state=NORMAL)

    def configui(self):
        configui = configUi.configUi(self.conf_file,self)
        self.stop_synchronize()
        self.disable()

    def parse_config_2_str(self,original_configs):
        str_configs = []

        for (k,conf) in original_configs.iteritems():
            str = "%s : %s -> %s " %(conf['number'],conf['source'],conf['target'])
            str_configs.append(str)

        return str_configs

    def write(self,text):
        if self.text_sum>10:
            self.text.configure(state=NORMAL)
            self.text.delete("0.0","2.0")
            self.text.configure(state=DISABLED)
            self.text_sum -= 1


        self.text_sum+=1
        self.text.configure(state=NORMAL)
        self.text.insert(END, "%s"%(text))
        self.text.see(END)
        splitter = text.split(':')
        if len(splitter) > 1:
            end = len(splitter[0])
            self.text.tag_add("here", "%d.0"%(self.text_sum), "%d.%d"%(self.text_sum,end))
            self.text.tag_config("here", background="yellow", foreground="blue")

        self.text.configure(state=DISABLED)



