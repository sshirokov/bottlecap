import re, os, sys
import operator

import bottle

from bottlecap.application import app

indexes_re = [r'^index.htm.?$', r'^index.']
indexes = [re.compile(i)
           for i in indexes_re]

def get_index_of(root):
    score = lambda m: m and operator.sub(*m.span()[::-1])
    match_all = lambda f: (i.match(f) for i in indexes)
    nth = lambda n: lambda l: l[n]
    nth_to = lambda n, to: lambda obj: to(nth(n)(obj))

    matches = [fname
               for (fname, score) in sorted([ (filename, max(match_all(filename))) for filename in os.listdir(root)
                                              if os.path.isfile(os.path.join(root, filename)) ],
                                            key=nth_to(1, score), reverse=True)
               if score]
    return matches and matches[0]

def maybe_index(root, path):
    joined = os.path.join(root, path)
    if os.path.isdir(joined):
        path = get_index_of(joined) or path
    return path

@app.get('/:path#.*?#', name='static')
def static(path):
    root = os.path.join(app.config['media_root'])
    return bottle.static_file(maybe_index(root, path),
                              root=root)
