# coding: euc-kr
import sys
from cx_Freeze import setup, Executable
executables = [Executable('D:/MyProjects/GreenMulti/GreenMulti.py', base='Win32GUI')]
setup(name='', version='0.0.0', description='None', executables=executables)