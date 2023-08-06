XPPRINT
=======

pretty-print of html


GETTING STARTED
---------------

    $ pip install xpprint
    $ curl -s http://www.pythonscraping.com/pages/page3.html | xpprint
    -html
    | -head
    | | -style
    | -body
    | | -div#wrapper
    | | | -img
    | | | -h1
    | | | -div#content
    | | | -table#giftList
    | | | | -tr
    | | | | | -th
    | | | | | -th
    | | | | | -th
    | | | | | -th
    | | | | -tr.gift#gift1
    | | | | | -td
    | | | | | -td
    | | | | | -td
    | | | | | -td
    | | | | | | -img
    | | | | -tr.gift#gift2
    | | | | | -td
    | | | | | -td
    | | | | | -td
    | | | | | -td
    | | | | | | -img
    | | | | -tr.gift#gift3
    | | | | | -td
    | | | | | -td
    | | | | | -td
    | | | | | -td
    | | | | | | -img
    | | | | -tr.gift#gift4
    | | | | | -td
    | | | | | -td
    | | | | | -td
    | | | | | -td
    | | | | | | -img
    | | | | -tr.gift#gift5
    | | | | | -td
    | | | | | -td
    | | | | | -td
    | | | | | -td
    | | | | | | -img
    -div#footer
    
    $ curl -s http://www.pythonscraping.com/pages/page3.html | xpprint --source --select "#gift3 > td:nth-child(1)"
      1,  0  -html
     23,  0  | -body
     24,  0  | | -div#wrapper
     33,  0  | | | -table#giftList
     65,  0  | | | | -tr.gift#gift3
     65, 28  | | | | | -td

    $ curl -s http://kondou.com/BS4/ | xpprint --text --select "#id2" --filter br
    -html
    | -body
    | | -div.document
    | | | -div.documentwrapper
    | | | | -div.bodywrapper
    | | | | | -div.body
    | | | | | | -div.section#beautiful-soup
    | | | | | | | -div.section#id2
    | | | | | | | | -h2                        (訳注)石鹸は食べられない
    | | | | | | | | | -a.headerlink            ¶
    | | | | | | | | -p                         この文書は
    | | | | | | | | | -a.reference external    Beautiful Soup 4.2.0
    | | | | | | | | -p                         2013年10月29日からこの文書の翻訳
    | | | | | | | | | -a.reference internal    パースツリーを修正
    | | | | | | | | -p                         誤訳やわかりづらいところを見つけたり、な
    | | | | | | | | | -img
    | | | | | | | | -p                         2013年10月現在、Beautiful
    | | | | | | | | -p
    | | | | | | | | | -strong                  混乱しないように初心者が知っておくべきこ
    | | | | | | | | -ul.simple
    | | | | | | | | | -li                      2012年5月にBS3の開発が終了し、現
    | | | | | | | | | -li                      BS3はPython3に対応していません
    | | | | | | | | | -li                      ただし、BS3のスクリプトのほとんどはi
    | | | | | | | | | -li                      そのため、BS3による情報も問題解決の役
    | | | | | | | | | -li                      詳しくは
    | | | | | | | | | | -a.reference internal  Beautiful Soup 3
    | | | | | | | | | -li                      この文書の
    | | | | | | | | | | -a.reference internal  クイックスタート
    | | | | | | | | | | -a.reference internal  find_all()


USAGE
-----

    $ xpprint -h
    usage: xpprint [-h] [--filter [FILTER [FILTER ...]]] [--parser PARSER]
                   [--source] [--select SELECT] [--raw] [--encoding ENCODING]
                   [--text]
                   [html]
    
    html tree view pprint
    
    positional arguments:
      html                  stdin or .html filename
    
    optional arguments:
      -h, --help            show this help message and exit
      --filter [FILTER [FILTER ...]]
                            filtered tag names (default: ['p', 'br', 'span'])
      --parser PARSER       HTML parser name (default: html.parser)
      --source              add "sourceline, pos" of corresponding start-tags
      --select SELECT       css selector string, must be quoted
      --raw                 add HTML below tree view, in the scope specified with
                            selector
      --encoding ENCODING   text encoding of stdin/stdout
      --text                add "text value" of corresponding tags


IMPORTANT LINKS
---------------

- The Tree Command for Linux Homepage -
  http://mama.indstate.edu/users/ice/tree/

- Collecting More Data from the Modern Web | Web Scraping with Python -
  http://www.pythonscraping.com/
