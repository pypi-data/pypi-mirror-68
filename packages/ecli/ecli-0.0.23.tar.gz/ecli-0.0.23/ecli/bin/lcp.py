from xdict.jprint import pobj 
from efdir import fs
import efuntool.efuntool as eftl
import sys
import elist.elist as elel
import estring.estring as eses

src = sys.argv[1]
s = fs.rfile(src)


dst = sys.argv[2]


start = int(eftl.dflt_sysargv(1,3)) - 1


line_sp = '\n' 
lines =  eses.split(s,line_sp) if(line_sp in s) else [s]
lngth = len(lines)


end = int(eftl.dflt_sysargv(lngth+1,4)) - 1




def main():
    global lines 
    lines = lines[start:end]
    s = elel.join(lines,line_sp)
    fs.wfile(dst,s)
