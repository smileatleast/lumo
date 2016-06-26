'''
SMART LAMP v2
bash command shortcut
KGARMIRE 
6.19.2016
'''
execfile("/home/pi/lumo/lumo.py")

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("first", type=str)
parser.add_argument("second", type=str)
args = parser.parse_args()

lumoRead(args.first, args.second)
