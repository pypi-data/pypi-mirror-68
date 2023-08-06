from xdict.jprint import pobj
from xdict.jprint import pdir
from xdict.cmdline import Hentry
from efdir import fs

from efdir import fs
import sys
import json
import elist.elist as elel

def load(o):
    h=''
    try:
        h = fs.rfile(o)
    except:
        h = o
    else:
        pass
    return(h)



def main_tagq():
    html_text = load(sys.argv[1])
    htry = Hentry(html_text=html_text)
    pls = sys.argv[2:]
    qstr = elel.join(pls,' ')
    html_entry = htry.query(qstr)

def main_attrq():
    html_text = load(sys.argv[1])
    htry = Hentry(html_text=html_text)
    korv = sys.argv[2]
    print('--in key----------:')
    html_entry = htry.query_attribs(korv,via='key')
    print('--in value----------:')
    html_entry = htry.query_attribs(korv,via='value')


def main_txtq():
    html_text = load(sys.argv[1])
    htry = Hentry(html_text=html_text)
    s = sys.argv[2]
    html_entry = htry.query_texts(s)



