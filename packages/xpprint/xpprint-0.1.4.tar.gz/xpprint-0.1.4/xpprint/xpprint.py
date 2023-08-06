import argparse
import math
import sys

from bs4 import BeautifulSoup, PageElement, Tag


def fmt_minimum(*, indent, name, cls, id, **kwargs):
    return '{indent}-{name}{cls}{id}'.format(indent=indent, name=name, cls=cls, id=id)


def fmt_source(*, indent, name, cls, id, srcinf, **kwargs):
    return '{srcinf}  {indent}-{name}{cls}{id}'.format(indent=indent, name=name, cls=cls, id=id, srcinf=srcinf)


def tree(bsObj, level=-1,
         filter=lambda x: False,
         formatter=fmt_minimum, digit=(3, 3),
         selector=""):
    assert isinstance(bsObj, PageElement), type(bsObj)
    
    if selector:
        bsObjSub = bsObj.select(selector)
        assert len(bsObjSub) == 1, 'css selector must correspond to 1 unique element. ()' % len(bsObjSub)
        
        bsObjCur = bsObjSub[0]
        while BeautifulSoup.ROOT_TAG_NAME != bsObjCur.name:
            for sibling in list(bsObjCur.next_siblings) + list(bsObjCur.previous_siblings):
                if isinstance(sibling, Tag):
                    sibling.decompose()
            bsObjCur = bsObjCur.parent
    
    if not isinstance(bsObj, Tag) or filter(bsObj.name):
        return
    
    if BeautifulSoup.ROOT_TAG_NAME != bsObj.name:
        indent = '| ' * max(level, 0)
        cls    = '.' + ' '.join(bsObj.attrs['class']) if 'class' in bsObj.attrs else ''
        id     = '#' + bsObj.attrs['id']              if 'id'    in bsObj.attrs else ''
        srcinf = str(bsObj.sourceline).rjust(digit[0]) + ',' + str(bsObj.sourcepos).rjust(digit[1])
        
        print(formatter(indent=indent,
                        cls=cls,
                        id=id,
                        name=bsObj.name,
                        srcinf=srcinf))
    
    for c in bsObj.children:
        tree(c, level=level+1, filter=filter, formatter=formatter, digit=digit)


def __digit(n):
    if n == 0:
        return 1
    else:
        return int(math.log10(abs(n))) + 1


def __source_digit(html):
    n = html.count('\n') + 1
    m = max([len(s) for s in html.split('\n')])
    
    return __digit(n), __digit(m)


def __parser():
    PARSER_DESC0 = 'html tree view pprint'
    PARSER_HELP0 = 'stdin or .html filename'
    PARSER_HELP1 = 'filtered tag names (default: %(default)s)'
    PARSER_HELP2 = 'HTML parser name (default: %(default)s)'
    PARSER_HELP3 = 'add "sourceline, pos" of corresponding start-tags'
    PARSER_HELP4 = 'css selector string, must be quoted'
    
    parser = argparse.ArgumentParser(description=PARSER_DESC0)
    parser.add_argument('html', nargs='?', type=argparse.FileType('r'), default=sys.stdin,
                        help=PARSER_HELP0)
    parser.add_argument('--filter', nargs='*', default=['p', 'br', 'span'],
                        help=PARSER_HELP1)
    parser.add_argument('--parser', default='html.parser',
                        help=PARSER_HELP2)
    parser.add_argument('--source', default=False, action='store_true',
                        help=PARSER_HELP3)
    parser.add_argument('--select',
                        help=PARSER_HELP4)
    
    return parser


parser = __parser()


def main():
    if sys.stdin.isatty():
        parser.print_help(); return
    
    args = parser.parse_args()
    html = args.html.read()
    bsObj = BeautifulSoup(html, features=args.parser)
    
    fmt = fmt_source if args.source else fmt_minimum
    flt = lambda x: x in args.filter
    dgt = __source_digit(html)
    sct = args.select
    
    tree(bsObj, filter=flt, formatter=fmt, digit=dgt, selector=sct)
