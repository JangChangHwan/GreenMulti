# coding: euc-kr
import sys
from cx_Freeze import setup, Executable
executables = [Executable('D:/GreenMulti/GreenMulti.py', base='Win32GUI')]
setup(name='d:/greenmulti/greenmulti.py', version='0.0.0', description='None', executables=executables)