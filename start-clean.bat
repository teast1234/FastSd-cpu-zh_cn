@echo off
set PATH=E:\fastsd\fastsdcpu\env;E:\fastsd\fastsdcpu\env\Scripts;E:\fastsd\fastsdcpu\env\Lib\site-packages\torch\lib;%SystemRoot%\System32;%SystemRoot%;%SystemRoot%\System32\Wbem
set MKL_THREADING_LAYER=GNU
env\Scripts\activate.bat
python src\app.py
pause