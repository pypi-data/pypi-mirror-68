from xdict.jprint import pobj 
from efdir import fs
import efuntool.efuntool as eftl
import sys
import elist.elist as elel
import estring.estring as eses

src = sys.argv[1]
s = fs.rfile(src)



start = int(eftl.dflt_sysargv(1,2)) - 1


line_sp = '\n' 
lines =  eses.split(s,line_sp) if(line_sp in s) else [s]
lngth = len(lines)


end = int(eftl.dflt_sysargv(lngth+1,3)) - 1


def main():
    global lines 
    arr0 = lines[0:start]
    arr1 = lines[end:lngth]
    lines = arr0+arr1
    s = elel.join(lines,line_sp)
    fs.wfile(src,s)
