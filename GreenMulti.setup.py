from cx_Freeze import setup, Executable
executables = [Executable('D:/MyProjects/GreenMulti/GreenMulti.py', base='Win32GUI')]
setup(name='D:/MyProjects/GreenMulti/GreenMulti.py', version='0.0.0', description='None', executables=executables)