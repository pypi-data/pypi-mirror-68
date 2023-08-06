from xdict.jprint import pobj 
from efdir import fs
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-path','-path',default='',help='dir path')
parser.add_argument('-start','-start',default='0',help='start line')
parser.add_argument('-end','-end',default='4294967296',help='end line')
parser.add_argument('-indent','-indent',default='4',help='indent')
parser.add_argument('-fixed_indent','-fixed_indent',default='False',help='fixed indent')
parser.add_argument('-with_color','-with_color',default='True',help='colorful display')
parser.add_argument('-key_color','-key_color',default='lightgreen',help='key color')
parser.add_argument('-value_color','-value_color',default='lightcyan',help='value color')
parser.add_argument('-list_ele_color','-list_ele_color',default='yellow',help='list element color')
parser.add_argument('-op_color','-op_color',default='white',help='operator color')
parser.add_argument('-default_color','-default_color',default='white',help='default color')
parser.add_argument('-spaces','-spaces', default=' ,\t',help='spaces')
parser.add_argument('-commas','-commas',default=',',help='commas')
parser.add_argument('-colons','-colons',default=':',help='colons')
parser.add_argument('-line_sps','-line_sps',default='\n,\r',help='line seperators')
parser.add_argument('-path_sps','-path_sps',default='/',help='path seperators')
parser.add_argument('-sp','-sp',default='/',help='seperator')

parser.add_argument('-blocks','-blocks',default='{}[]()<>',help='block pairs')
parser.add_argument('-quotes','-quotes',default='\'\'\"\"',help='quote pairs')





def boolstr2bool(s):
    if(s.lower() == 'false'):
        return(False)
    else:
        return(True)


args=parser.parse_args()
p = args.path
d = fs.rfile(p) if(fs.filexist(p)) else p
d = eval(d)
start = int(args.start)
end = int(args.end)
indent = int(args.indent)
fixed_indent = boolstr2bool(args.fixed_indent)
with_color = boolstr2bool(args.with_color)
key_color = args.key_color
value_color = args.value_color
list_ele_color = args.list_ele_color
op_color = args.op_color
default_color = args.default_color
sp = args.sp
line_sps = args.line_sps.split(',')
path_sps = args.path_sps.split(',')
commas = args.commas.split('/')
colons = args.colons.split(',')
spaces = args.spaces.split(',')
blocks = args.blocks
quotes = args.quotes


def main():
    pobj(
        d,
        start=start,
        end=end,
        indent=indent, 
        fixed_indent=fixed_indent,
        with_color=with_color,
        key_color=key_color,
        value_color=value_color,
        list_ele_color=list_ele_color,
        op_color=op_color,
        default_color=default_color, 
        sp=sp,
        line_sps=line_sps,
        path_sps=path_sps,
        commas=commas,
        colons=colons,
        spaces=spaces,
        quotes_pairs=quotes,
        block_op_pairs=blocks
    ) 
