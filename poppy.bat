if "%1" == "h" goto begin
mshta vbscript:createobject("wscript.shell").run("%~nx0 h",0)(window.close)&&exit
:begin

set dir=%~dp0

echo %PATH%

start pythonw %dir%/poppy.py