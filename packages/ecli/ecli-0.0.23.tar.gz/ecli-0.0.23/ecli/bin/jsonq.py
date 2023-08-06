from xdict import cmdline
from xdict.jprint import pobj
from efdir import fs
import sys
import json
import elist.elist as elel

def load(o):
    j=None
    try:
        j = fs.rjson(o)
    except:
        try:
            s = fs.rfile(o)
            j = eval(s)
        except:
            j = eval(o)    
        else:
            pass        
    else:
        pass
    return(j)




def main():
    j = load(sys.argv[1])
    pl = sys.argv[2:]
    cmdk = elel.join(pl,' ')
    cmdt = cmdline.cmdict(dict=j,debug=0)
    r = cmdt[cmdk]
    if(r):
        pobj(r)
    else:
        pass


