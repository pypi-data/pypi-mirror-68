from ecli.abbr import get_word_abbr
from efdir import fs
from xdict.jprint import pobj

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-str','-str',default='',help='string')
parser.add_argument('-file','-file',default='',help='file')
parser.add_argument('-regex','-regex',default='[-_ ]',help='regex')

args=parser.parse_args()
s = args.str
f = args.file
r = args.regex

def main():
    global s;
    global f;
    global r;
    unhandled = []
    if(s):
        unhandled = s.split(',')
    elif(f):
        try:
            unhandled = fs.rjson(f)
        except:
            s = fs.rfile(f)
            s = s.strip('\n')
            unhandled = s.split('\n')
        else:
            pass
    else:
        pass
    print(unhandled)
    abbr = get_word_abbr(unhandled)
    pobj(abbr)
