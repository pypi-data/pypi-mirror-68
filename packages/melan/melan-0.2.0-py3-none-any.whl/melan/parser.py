
from nxp import Num, Bool, FileBuffer, ListBuffer, make_parser

# ------------------------------------------------------------------------

def _saveIndent(c,x,m):
    x.set('indent',c.line.prelen)
def _checkIndent(c,x):
    return c.line.prelen <= x.get('indent',1)
def _nobreak(c,x,m):
    if c.eol: c.error('No linebreaks allowed in strings.')
    return True

# language definition using NXP
_variable = [ r'\$\{(\w[:.\w]*)\}', ('tag','var') ]
_command = [ r'\\(\w[:\w]*)', ('open','command'), ('tag','cmd') ]
_comment = [ r'#.*$', ('tag','com') ]
_tilde = [ r'~', ('rep','') ]

Language = {
    'main': [
        [ r'\s*$|\s+' ], # consume spaces
        _comment,
        _command,
        [ r'^\s*@begin\s*$', ('open','document'), ('tag','doc') ],
        [ r'@\{begin\}', ('open','document'), ('tag','doc') ]
    ],
    'document': [
        [ r'[^\\$#@~]+' ], # optimization
        [ r'\\[\\$#~]', ('proc',lambda t: t[1]), ('tag','rep') ],
        _comment,
        _tilde,
        _variable,
        _command,
        [ r'^\s*@end\s*$', ('tag','/doc'), 'close' ],
        [ r'@\{end\}', ('tag','/doc'), 'close' ]
    ],
    'command': {
        'main': [
            [ r'\(', ('open','command.option'), ('tag','grp') ],
            [ r'\{', ('open','command.body_curly'), ('tag','curly') ],
            [ r'\[', ('open','command.body_square'), ('tag','square') ],
            [ r'<\[', ('open','command.body_angle'), ('tag','angle') ],
            [ None, 'close' ]
        ],
        'option': {
            'main': [
                [ r'\s+' ], # consume spaces
                [ r'\)', ('tag','/grp'), 'close' ],
                [ r'\w+', ('open','command.option.name'), ('tag','opt') ]
            ],
            'name': [
                [ r'\s+' ], # consume spaces
                [ r',', 'close' ], # equivalence: foo, <=> foo=True,
                [ r'=', ('open','command.option.value') ],
                [ r'\)', 'close', ('tag','/grp'), 'close' ]
            ],
            'value': [
                [ r'"', ('swap','command.option.dq_string'), ('tag','str') ],
                [ r"'", ('swap','command.option.sq_string'), ('tag','str') ],
                [ Num(), ('tag','num'), 'close' ],
                [ Bool(), ('tag','bool'), 'close' ]
            ],
            'dq_string': [
                [ r'[^\\"$]+', ('valid',_nobreak) ], # optimization
                [ r'$', ('err','No linebreaks allowed in strings.') ],
                _variable,
                [ r'\\"' ],
                [ r'"', ('tag','/str'), 'close' ]
            ],
            'sq_string': [
                [ r"[^\\']+", ('valid',_nobreak) ], # optimization
                [ r'$', ('err','No linebreaks allowed in strings.') ],
                [ r"\\'" ],
                [ r"'", ('tag','/str'), 'close' ]
            ]
        },
        'body_curly': [
            [ r'[^\\$#}~]+' ], # optimization
            [ r'\\[\\$#{}~]', ('proc',lambda t: t[1]), ('tag','rep') ],
            _comment,
            _tilde,
            _variable,
            _command,
            [ r'}', ('tag','/curly'), ('close',2) ]
        ],
        'body_square': [
            [ r'[^\\\]]+' ], # optimization
            [ r'\\[\\\[\]]', ('proc',lambda t: t[1]), ('tag','rep') ],
            [ r'\]', ('tag','/square'), ('close',2) ]
        ],
        'body_angle': [
            [ r'[^\\\]]+' ], # optimization
            [ r'\\(\\|<\[|\]>)', ('proc',lambda t: t[1:]), ('tag','rep') ],
            [ r'\]>', ('tag','/angle'), ('close',2) ]
        ]
    }
}

# ------------------------------------------------------------------------

Parser = make_parser({
    'lang': Language,
    'strict': [
        'main',
        'command.option',
        'command.option.name',
        'command.option.value'
    ],
    'end': 'main'
})
