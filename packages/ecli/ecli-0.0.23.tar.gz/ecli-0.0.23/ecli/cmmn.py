import sys
import os
import subprocess
import shlex
import re
import estring.estring as eses
from efdir import fs
import elist.elist as elel
from xdict.jprint import pobj

TREE_CONN_DICT = {
    "arr":[chr(9500),chr(9472),chr(9474),chr(9492)],
    "regex":re.compile('['+chr(9500)+chr(9472)+chr(9474)+chr(9492)+']+'),
}

def pipe_shell_cmds(cmds,rtrn_code=False):
    lngth = len(cmds)
    p={}
    p[0] = subprocess.Popen(
        shlex.split(cmds[0]),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE 
    )
    for i in range(1,lngth):
        p[i] = subprocess.Popen(
            shlex.split(cmds[1]),
            stdin=p[i-1].stdout,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    rslt = p[lngth-1].communicate()    
    if(lngth>1):
        for i in range(1,lngth):
            code = p[i].wait()
    else:
        code = p[lngth-1].wait()
    rslt = rslt[0].decode()  
    if(rtrn_code):
        return({'rslt':rslt,'code':code})
    else:    
        return(rslt)   


def srch(s,fn):
    d = {}
    fn = '.' if(fn=='') else fn
    fl = fs.walkf(fn)
    cmdsl = elel.mapv(fl,lambda f:['cat '+f,' egrep "'+s+'"'])
    for i in range(len(cmdsl)):
        cmds = cmdsl[i] 
        rslt = pipe_shell_cmds(cmds)
        if(rslt==""):
            pass
        else:
            cmd = fl[i]   
            d[cmd] = rslt
    pobj(d)
    return(d)
