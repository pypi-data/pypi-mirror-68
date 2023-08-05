
from .util import *
from .helper import *
from .parser import Parser
from .prefix import PrefixTree

from importlib import import_module
from warnings import warn
from os import getcwd, chdir
import os.path as op
import json
import sys
import re

import nxp
from nxp.error import ScopeError, TagError, LengthError
from nxp.util import Hub as EventHub

# ------------------------------------------------------------------------

class Compiler:

    __slots__ = ('_pre','_doc','_var','_fmt','_evt','_path','_stack','_indoc')
    def __init__( self ):
        self._pre = dict()
        self._doc = dict()
        self._var = PrefixTree('warn')
        self._fmt = Format('default')
        self._evt = EventHub()
        self._path = [ '.' ]

        # create events and initialize stack
        for chan in ['load','new.var','new.pre','new.doc','doc.begin','doc.end','cmd.begin','cmd.end']:
            self._evt.create(chan)
        
        self._stack = Stack(self)

        # initialize path and built-in commands
        sys.path.insert( 0, getcwd() )
        self.load('melan.builtin',dom='')

    @property 
    def stack(self): return self._stack
    @property 
    def indoc(self): return self._stack.indoc
    @property
    def format(self): return self._fmt

    # ----------  =====  ----------
    # main functions

    def process(self,buffer,first=(0,0),last=None):
        tsf = nxp.procbuf( Parser, self._callback, buffer, first, last )
        txt = str(tsf)
        return self._fmt(self,txt)

    def procfile(self,infile,r2l=False):
        fpath = self.pathFind(infile)
        with file_buffer( fpath, r2l ) as buf:
            return self.process(buf)

    def proctext(self,text,r2l=False):
        buf = nxp.ListBuffer( text.splitlines(True), r2l )
        return self.process(buf)

    def __str__(self):
        pre = ', '.join([ self._pre.keys() ])
        doc = ', '.join([ self._doc.keys() ])
        var = ', '.join([ self._var.keys() ])

        return '\n'.join([
            'MeLan compiler', 
            '+ Path:\n\t' + ' ; '.join(self._path),
            f'+ Variables ({len(self._var)}):\n\t{var}',
            f'+ Preamble ({len(self._pre)}):\n\t{pre}',
            f'+ Document ({len(self._doc)}):\n\t{doc}'
        ])

    # ----------  =====  ----------
    # event-related

    def publish( self, _chan, *args, **kwargs ):
        self._evt.publish(_chan,*args,**kwargs)
        return self

    def subscribe( self, _chan, fun ):
        return self._evt.subscribe(_chan,fun)

    # ----------  =====  ----------
    # variables

    def varAdd(self,var,prefix=''): 
        # convert to dict
        if isinstance(var,str):
            assert op.isfile(var), FileNotFoundError(var)
            assert var.endswith('.json'), ValueError('Not a JSON file.')
            with open(var) as fh:
                return json.load(fh)
        
        assert isinstance(var,dict), TypeError(f'Bad var type: {type(var)}')
        self.publish( 'new.var', data=var )

        # insert each item
        for k,v in var.items():
            self._var.insert( prefix+k, v )

        return self
    def varFilt(self,prefix):
        return { k.lstrip(prefix): v for k,v in self._var.filter(prefix) }

    def lst(self,key): return self._var.setdefault(key,[])
    def arg(self,key): return self._var.setdefault(key,{})
    def num(self,key): return self._var.setdefault(key,0)
    def get(self,key,default=None): return self._var.setdefault(key,default)

    def __getitem__(self,key): 
        return self._var[key]
    def __setitem__(self,key,val): 
        self._var[key] = val
    def __contains__(self,key):
        return key in self._var

    # ----------  =====  ----------
    # path, files, and extensions

    def pathAppend(self,p):
        p = _sanitize_folder(p)
        if p not in self._path:
            self._path.append(p)
        return self
    def pathPrepend(self,p):
        p = _sanitize_folder(p)
        if p not in self._path:
            self._path.insert(0,p)
        return self
    def pathFind(self,f):
        for p in self._path:
            q = op.join(p,f)
            if op.exists(q):
                return q
        raise FileNotFoundError(f)

    def readfile(self,f):
        with open(self.pathFind(f)) as fh:
            return fh.read()

    # ----------  =====  ----------
    # commands

    def import_export(self,name,package=None,dom='melan_'):
        # remove .py extension
        if name.endswith('.py') and op.isfile(name):
            name = name.rstrip('.py')

        # import module and look for "export"
        name = dom+name
        export = import_module( name, package )
        try:
            export = export.export 
        except:
            raise RuntimeError(f'"export" variable not found in module: {name}')

        return export

    def load_dict(self,x,prefix=''):
        assert isinstance(x,dict), TypeError(f'Unexpected type: {type(x)}')

        # validate prefix
        if prefix: 
            assert re.match( r'\w[:\w]*', prefix ), ValueError(f'Invalid prefix: {prefix}')
            if not prefix.endswith(':'): prefix += ':'

        self.publish( 'load', data=x, prefix=prefix )

        # process input
        if 'ini' in x: x['ini'](self)
        if 'pre' in x: self.preAdd(x['pre'],prefix)
        if 'doc' in x: self.docAdd(x['doc'],prefix)
        if 'var' in x: self.varAdd(x['var'])
        if 'fmt' in x: self._fmt = x['fmt']

        assert isinstance(self._fmt,Format), TypeError(f'Unexpected format type: {type(self._fmt)}')
        return self

    def load(self,name,prefix='',package=None,dom='melan_'):
        export = self.import_export(name,package,dom)
        return self.load_dict(export,prefix)

    def _addcmd(self,attr,cmd,prefix):
        # validate
        assert isinstance(cmd,dict), \
            TypeError(f'Expected dict, but got "{type(cmd)}" instead.')
        assert all([ callable(f) for f in cmd.values() ]), \
            TypeError('Command values should be callable.')

        # get corresponding dict property
        prop = getattr(self,'_'+attr)
        self.publish( 'new.'+attr, cmd=cmd, prefix=prefix )

        # add commands one by one
        override = []
        for name,fun in cmd.items():
            name = prefix+name
            if name in prop: override.append(name)
            prop[name] = fun

        # notify about overrides
        if override:
            override = ', '.join(override)
            warn( f'Command override ({attr}): {override}', Warning )

        return self

    def preAdd(self,cmd,prefix=''):
        return self._addcmd( 'pre', cmd, prefix )

    def docAdd(self,cmd,prefix=''):
        return self._addcmd( 'doc', cmd, prefix )

    # ----------  =====  ----------
    # processing callback

    def _callback(self,tsf,elm):
        if isinstance(elm,nxp.RMatch):
            beg,end = elm.beg, elm.end
            tag = elm.tag 

            if tag == 'rep':
                tsf.sub( beg, end, elm.text )
            elif tag == 'var':
                tsf.sub( beg, end, self[elm[1]] )
            elif tag == 'com':
                tsf.clear( beg, end )
            else:
                raise TagError(tag,'Unknown tag')
        elif elm.name == 'command':
            self._cb_cmd(tsf,elm)
        elif elm.name == 'document':
            self._cb_doc(tsf,elm)
        else:
            raise ScopeError(elm.name,'Unexpected scope')

    def _cb_doc(self,tsf,elm):
        assert not self._stack.indoc, RuntimeError('[bug] Nested document?')
        assert len(elm) >= 2, LengthError(elm)

        # bounds
        _surrounding_tags_match(elm)
        tsf.restrict( elm[0].end, elm[-1].beg )
        
        # process
        self.publish( 'doc.begin' )
        for sub in elm[1:-1]: self._callback(tsf,sub)
        self.publish( 'doc.end' )
        
    def _cb_cmd(self,tsf,elm):
        assert len(elm) <= 3, LengthError(elm)

        # command name
        match = elm[0]
        assert match.tag == 'cmd', TagError(match.tag)

        name = match.data[1]
        beg,end = match.beg, match.end
        self.publish( 'cmd.begin', name=name, pos=beg )

        # body and options
        body = ''
        opt = dict()
        buf = tsf.buffer

        for sub in elm[1:]:
            assert isinstance(sub,nxp.RNode), TypeError(sub)
            if sub.name == 'command.option':
                _,e,opt = self._cb_opt(buf,sub)
            else:
                _,e,body = self._cb_body(buf,sub)
            
            if e > end: end = e

        # call command
        if self._stack.indoc:
            tsf.sub( beg, end, self._doc[name](body,**opt) )
        else:
            self._pre[name](self,body,**opt)

        self.publish( 'cmd.end', name=name, pos=end )

    def _cb_opt(self,buf,elm):
        assert len(elm) >= 2, LengthError(elm,'Insufficient length')

        # bounds
        _surrounding_tags_match(elm)
        beg, end = elm[0].beg, elm[-1].end

        # options
        out = dict()
        for sub in elm[1:-1]:
            assert sub.name == 'command.option.name', ScopeError(sub.name)
            assert 1 <= len(sub) <= 2, LengthError(sub)
            assert sub[0].tag == 'opt', TagError(sub[0].tag)

            name = sub[0].text
            if len(sub) > 1:
                out[name] = self._cb_val(buf,sub[1])
            else:
                out[name] = True 

        return beg,end,out

    def _cb_val(self,buf,elm):
        assert elm.name.startswith('command.option.'), ScopeError(elm.name)
        tag = elm[0].tag 
        if tag == 'num':
            return float(elm[0].text)
        elif tag == 'bool':
            txt = elm[0].text.lower()
            return { 'true': True, 'false': False }[txt]
        else:
            return self._cb_str(buf,elm)

    def _cb_str(self,buf,elm):
        assert len(elm) >= 2, LengthError(elm,'Insufficient length')

        # process matches within quotes
        tsf = nxp.Transform( buf, elm[0].end, elm[-1].beg )
        for sub in elm[1:-1]: self._callback(tsf,sub)
        return str(tsf)

    def _cb_body(self,buf,elm):
        assert len(elm) >= 2, LengthError(elm,'Insufficient length')

        # beginning/end of body delimiters
        _surrounding_tags_match(elm)
        beg = elm[0].beg 
        end = elm[-1].end
        
        # process matches within delimiters
        tsf = nxp.Transform( buf, elm[0].end, elm[-1].beg )
        for sub in elm[1:-1]: self._callback(tsf,sub)

        # remove common indent for multiline bodies
        return beg,end,str(tsf)

# ------------------------------------------------------------------------

def _surrounding_tags_match(elm):
    first = elm[0]
    last = elm[-1]
    assert first.tag == last.tag[1:], \
        TagError( f'{first.tag} vs. {last.tag}', 'Tag mismatch between first and last elements.' )

def _sanitize_folder(path):
    assert op.isdir(path), NotADirectoryError(f'Not a folder: {path}')
    return op.realpath(path)
