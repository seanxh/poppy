poppy
=====

Poppy可以同步两个本地文件夹中的内容。

使用

依赖关系：

poppy的文件消息机制依赖于watchdog 扩展。使用前需要先安装watchdog
WatchDog主页：http://pythonhosted.org//watchdog
安装：
http://pythonhosted.org//watchdog/installation.html#installation
示例：
$ wget -c http://pypi.python.org/packages/source/w/watchdog/watchdog-0.7.1.tar.gz
$ tar zxvf watchdog-0.7.1.tar.gz
$ cd watchdog-0.7.1
$ python setup.py install

配置：

编辑 config.py

在DIRS中增加你想要同步的文件夹。

格式如下：
[r"DIR1",r"DIR2",[strict dirs][patterns]]

例如：
[r"D:/poppy/",r"Z:/poppy/",["child_dir1","child/child_dir"],['.*\.php','.*\.py']]

关于强制文件夹：

当你定义了一个非空的Strict Dirs列表时，程序初始化时就会检查两个文件夹的不同。如果确实有不同，你必须按yes同步。

启动：
python main.py

====================

poppy can synchronize two local dir's content.

How to Use

Depend on

poppy use the watchDog to receive the OS's file changed notify, which should be installed before you use poppy.

WatchDog HomePage :http://pythonhosted.org//watchdog

Install:
http://pythonhosted.org//watchdog/installation.html#installation

EG:
$ wget -c http://pypi.python.org/packages/source/w/watchdog/watchdog-0.7.1.tar.gz
$ tar zxvf watchdog-0.7.1.tar.gz
$ cd watchdog-0.7.1
$ python setup.py install

Config

Edit config.py

add the dir to variable DIR which you want to synchronized.

Format:
[r"DIR1",r"DIR2",[strict dirs][patterns]]

Eg:
[r"D:/poppy/",r"Z:/poppy/",["child_dir1","child/child_dir"],['.*\.php','.*\.py']]

About Strict Dirs:
If you defined the third parameter and not a empty list.

When the program start, it will check the difference between the two child dir. When it is True,you will have to enter "yes" to synchronize the strict DIRs.

Start
python main.py