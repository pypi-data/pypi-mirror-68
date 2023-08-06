from ecli.cmmn import srch

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-str','-str',default='',help='srch string')
parser.add_argument('-path','-path',default='',help='dir path')

args=parser.parse_args()
s = args.str
p = args.path

def main():
    srch(s,p)
