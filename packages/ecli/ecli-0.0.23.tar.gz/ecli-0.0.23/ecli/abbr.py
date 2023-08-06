HTML_TAGS = ['a', 'abbr', 'acronym', 'address', 'applet', 'area', 'article', 'aside', 'audio', 'b', 'base', 'basefont', 'bdi', 'bdo', 'big', 'blockquote', 'body', 'br', 'button', 'canvas', 'caption', 'center', 'cite', 'code', 'col', 'colgroup', 'command', 'datalist', 'dd', 'del', 'details', 'dir', 'div', 'dfn', 'dialog', 'dl', 'dt', 'em', 'embed', 'fieldset', 'figcaption', 'figure', 'font', 'footer', 'form', 'frame', 'frameset', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'head', 'header', 'hr', 'html', 'i', 'iframe', 'img', 'input', 'ins', 'isindex', 'kbd', 'keygen', 'label', 'legend', 'li', 'link', 'map', 'mark', 'menu', 'menuitem', 'meta', 'meter', 'nav', 'noframes', 'noscript', 'object', 'ol', 'optgroup', 'option', 'output', 'p', 'param', 'pre', 'progress', 'q', 'rp', 'rt', 'ruby', 's', 'samp', 'script', 'section', 'select', 'small', 'source', 'span', 'strike', 'strong', 'style', 'sub', 'summary', 'sup', 'table', 'tbody', 'td', 'textarea', 'tfoot', 'th', 'thead', 'time', 'title', 'tr', 'track', 'tt', 'u', 'ul', 'var', 'video', 'wbr', 'xmp']




import elist.elist as elel
import estring.estring as eses
import re
import edict.edict as eded
import copy

def get_next_unhandled(cdict,abbr):
    next_unhandled = []
    for k in cdict:
        l = cdict[k]
        if(len(l) == 1):
            abbr[k] = l[0]
        else:
            if(k in l):
                abbr[k] = k
                l.remove(k)
                next_unhandled = next_unhandled + l
            else:
                next_unhandled = next_unhandled + l
    return(next_unhandled,abbr)


def get_one_word_abbr(unhandled):
    abbr = {}
    c = 1
    while(len(unhandled)>0):
        cdict  = elel.groupby_head_str(unhandled,c)
        unhandled,abbr = get_next_unhandled(cdict,abbr)
        c = c + 1
    return(abbr)


def padding_entry(entry):
    width = max(elel.mapv(entry,lambda r:len(r)))
    entry = elel.mapv(entry,lambda r:eses.padEnd(r,width))
    return(entry)

def get_word_abbr(ounhandled,regex = re.compile('[-_ ]')):
    cond = isinstance(regex,type(re.compile('')))
    regex = regex if(cond) else re.compile(regex)
    unhandled = elel.mapv(ounhandled,lambda r:eses.split(r,regex))
    unhandled = elel.mapv(unhandled,lambda r:padding_entry(r))
    unhandled = elel.mapv(unhandled,lambda r:elel.interleave(*r))
    unhandled = elel.mapv(unhandled,lambda r:elel.join(r,''))
    refd = eded.kvlist2d(unhandled,ounhandled)
    abbr = get_one_word_abbr(unhandled)
    for k in abbr:
        v = abbr[k]
        abbr[k] = refd[v]
    return(abbr)
