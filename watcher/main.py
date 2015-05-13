__author__ = 'sean'
from utils import *
import threading
from task import *
from watcher import *

class Main(object):

    def __init__(self,source,target,strict,exclude,include,console=sys.stderr):
        self.source = source
        self.target = target
        self.strict = strict
        self.include = include
        self.exclude = exclude
        self.console = console
        self.work = None
        self.source_watcher = None

    def init_global_lock(self,*dirs):
        GlobalVariable.locks = {}
        GlobalVariable.dirs = []
        for dir in dirs:
            GlobalVariable.locks[dir] = threading.Lock()
            GlobalVariable.dirs.append( dir )

    def start(self):
        if not os.path.isdir(self.source) :
            self.console.write("the dir %s is not exit! Start Fail" %(self.source))
            return False
        elif not os.path.isdir(self.target):
            self.console.write("the dir %s is not exit! Start Fail" %(self.target))
            return False

        self.init_global_lock(self.source,self.target)

        GlobalVariable.init = True
        self.work=Worker(console=self.console)

        self.source_watcher = Watcher(self.source,self.exclude,self.include)
        self.source_watcher.start()
        self.work.start()
        self.console.write( "All init job is done,Synchronizing\n")
        return True

    def stop(self):
        if self.source_watcher is not None and self.source_watcher.is_alive():
            self.source_watcher.stop()
            self.source_watcher.join()
            self.source_watcher = None
        if self.work is not None and self.work.is_alive():
            self.work.stop()
            self.work.join()
            self.work = None
