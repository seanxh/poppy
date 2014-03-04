poppy
=====

poppy can synchronize two local dir's content.

How to Use

Config

Edit config.py

add the dir to variable DIR which you want to synchronized.

Format:
[r"DIR1",r"DIR2",[patterns]]

Eg:
[r"D:/poppy/",r"Z:/poppy/",['.*\.php','.*\.py']]

Start
python main.py

====================


Poppy可以同步两个本地文件夹中的内容。

使用

配置：

编辑 config.py

在DIRS中增加你想要同步的文件夹。

格式如下：
[r"DIR1",r"DIR2",[patterns]]

例如：
[r"D:/poppy/",r"Z:/poppy/",['.*\.php','.*\.py']]

启动：
python main.py