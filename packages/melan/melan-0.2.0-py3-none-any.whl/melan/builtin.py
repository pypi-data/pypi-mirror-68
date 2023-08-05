
import os.path as op
import json
import sys 

# ------------------------------------------------------------------------

_cpl = None

def init(cpl):
    global _cpl
    _cpl = cpl

#-------------------------------------------------------------
# Preamble commands
#-------------------------------------------------------------

def addpath(cpl,path,before=False):
    assert op.isdir(path), NotADirectoryError(f'Not a folder: {path}')
    path = op.realpath(path)
    if before:
        cpl.pathPrepend(path)
    else:
        cpl.pathAppend(path)

def pypath(cpl,path,before=False):
    assert op.isdir(path), NotADirectoryError(f'Not a folder: {path}')
    path = op.realpath(path)
    if before:
        sys.path.insert(0,path)
    else:
        sys.path.append(path)

def usepkg(cpl,path,prefix='',package=None):
    cpl.load(path,prefix=prefix,package=package)

def _define(cpl,*args,**kv):
    define(*args,**kv)

#-------------------------------------------------------------
# Document commands
#-------------------------------------------------------------

def define(body=None,_file=None,**kv):
    if body:
        _cpl.varAdd(json.loads(body))
    if _file:
        _cpl.varAdd(_file)
    if kv:
        _cpl.varAdd(dict(kv))

def include(body,r2l=False,raw=False):
    if raw:
        return _cpl.readfile(body)
    else:
        return _cpl.procfile(body,r2l)

def verbatim(body):
    return body

# ------------------------------------------------------------------------

export = {
    'name': 'builtin',
    'ini': init,
    'pre': {
        'addpath': addpath,
        'pypath': pypath,
        'usepkg': usepkg,
        'define': _define
    },
    'doc': { 
        'define': define,
        'include': include,
        'verbatim': verbatim
    }
}
