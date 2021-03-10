#!/bin/python3
import os

dira = os.getcwd()
print(dira)
tempdir="//tmp"
dirb = os.chdir(tempdir)
dirb = os.getcwd()
print(dirb)
