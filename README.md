Poppy
=====

Poppy是一个简单的用于同步两个本地文件夹中文件的工具。

## 操作系统
poppy是用python语言编写,GUI界面使用Tkinter完成。原则上来说兼容Win/Linux/Mac。针对Win&Mac下的兼容性进行了常规测试，欢迎Linux用户反馈。

## 依赖关系
poppy的文件变更消息机制依赖于py-watchdog。使用前需要先安装watchdog

WatchDog主页：http://pythonhosted.org//watchdog

## 安装参考
http://pythonhosted.org//watchdog/installation.html#installation

### Linux/Mac OSX 安装示例：
```
$ wget -c http://pypi.python.org/packages/source/w/watchdog/watchdog-0.7.1.tar.gz
$ tar zxvf watchdog-0.7.1.tar.gz
$ cd watchdog-0.7.1
$ python setup.py install
```

## 配置
Poppy的配置信息在config/config.ini文件中，一般除非您使用命令行界面或备份配置信息，不需要手动修改此配置文件。

## 启动
Windows请直接执行poppy.bat脚本启动Poppy程序界面。

Linux/Mac OSX 用户可直接招待poppy脚本以启动。


## 反馈
seanxuhao@gmail.com

Poppy
====================

Poppy is a simple and reliable tool for synchronizing two directories contents. 

## Operate System:
poppy is written by python, and GUI is written by py-Tkiner.In principle it can compat with Windows/Linux/Mac.
I tested for Windows and Mac OSX, and welcome the Linux's test.


## Depend on
poppy uses the py-watchDog to receive the OS's file changed notify, which should be installed before you use poppy.

WatchDog HomePage :http://pythonhosted.org//watchdog

## Install reference
http://pythonhosted.org//watchdog/installation.html#installation

### Linux/MacOS install demo:
```
$ wget -c http://pypi.python.org/packages/source/w/watchdog/watchdog-0.7.1.tar.gz
$ tar zxvf watchdog-0.7.1.tar.gz
$ cd watchdog-0.7.1
$ python setup.py install
```

## Configure

poppy's config file is written in config/config.ini. Unless you use the command model or you want to back up the config, otherwise you will not care this file.

## Start

Windows user can execute the poppy.bat for running the GUI of Poppy Application.

Mac OSX/Linux user can execute poppy shell script to running it.

## Feedback
[seanxuhao@gmail.com](seanxuhao@gmail.com)