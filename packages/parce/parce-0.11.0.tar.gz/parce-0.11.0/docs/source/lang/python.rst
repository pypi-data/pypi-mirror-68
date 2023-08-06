python
======

.. automodule:: parce.lang.python
    :members:
    :undoc-members:
    :show-inheritance:

Example:
--------

Root lexicon ``Python.root`` and text:

.. code-block:: python

    #! /usr/bin/env python3
    
    # Python test file
    
    CASE_CONSTANT = 100.367e-12
    
    import sys
    
    def func(a):
        return [i + 1 for i in range(a)]
    
    result = 2
    print(f"The result is {result}.")
    

Result tree::

    <Context Python.root at 0-181 (22 children)>
     ├╴<Token '#' at 0:1 (Comment)>
     ├╴<Context Python.comment at 1-23 (1 child)>
     │  ╰╴<Token '! /usr/bin/env python3' at 1:23 (Comment)>
     ├╴<Token '#' at 25:26 (Comment)>
     ├╴<Context Python.comment at 26-43 (1 child)>
     │  ╰╴<Token ' Python test file' at 26:43 (Comment)>
     ├╴<Token 'CASE_CONSTANT' at 45:58 (Name.Constant)>
     ├╴<Token '=' at 59:60 (Delimiter.Operator.Assignment)>
     ├╴<Token '100.367e-12' at 61:72 (Literal.Number)>
     ├╴<Token 'import' at 74:80 (Keyword)>
     ├╴<Token 'sys' at 81:84 (Name.Variable)>
     ├╴<Token 'def' at 86:89 (Keyword)>
     ├╴<Token 'func' at 90:94 (Name.Function.Definition)>
     ├╴<Context Python.funcdef at 94-98 (3 children)>
     │  ├╴<Token '(' at 94:95 (Delimiter)>
     │  ├╴<Context Python.signature at 95-97 (2 children)>
     │  │  ├╴<Token 'a' at 95:96 (Name.Variable)>
     │  │  ╰╴<Token ')' at 96:97 (Delimiter)>
     │  ╰╴<Token ':' at 97:98 (Delimiter.Indent)>
     ├╴<Token '    ' at 99:103 (Whitespace.Indent)>
     ├╴<Token 'return' at 103:109 (Keyword)>
     ├╴<Token '[' at 110:111 (Delimiter)>
     ├╴<Context Python.list at 111-135 (10 children)>
     │  ├╴<Token 'i' at 111:112 (Name.Variable)>
     │  ├╴<Token '+' at 113:114 (Delimiter.Operator)>
     │  ├╴<Token '1' at 115:116 (Literal.Number)>
     │  ├╴<Token 'for' at 117:120 (Keyword)>
     │  ├╴<Token 'i' at 121:122 (Name.Variable)>
     │  ├╴<Token 'in' at 123:125 (Keyword)>
     │  ├╴<Token 'range' at 126:131 (Name.Builtin)>
     │  ├╴<Token '(' at 131:132 (Delimiter)>
     │  ├╴<Context Python.call at 132-134 (2 children)>
     │  │  ├╴<Token 'a' at 132:133 (Name.Variable)>
     │  │  ╰╴<Token ')' at 133:134 (Delimiter)>
     │  ╰╴<Token ']' at 134:135 (Delimiter)>
     ├╴<Token 'result' at 137:143 (Name.Variable)>
     ├╴<Token '=' at 144:145 (Delimiter.Operator.Assignment)>
     ├╴<Token '2' at 146:147 (Literal.Number)>
     ├╴<Token 'print' at 148:153 (Name.Builtin)>
     ├╴<Token '(' at 153:154 (Delimiter)>
     ╰╴<Context Python.call at 154-181 (4 children)>
        ├╴<Token 'f' at 154:155 (Literal.String.Prefix)>
        ├╴<Token '"' at 155:156 (Literal.String.Start)>
        ├╴<Context Python.string at 156-180 (1 child)>
        │  ╰╴<Context Python.short_string_format* at 156-180 (5 children)>
        │     ├╴<Token 'The result is ' at 156:170 (Literal.String)>
        │     ├╴<Token '{' at 170:171 (Delimiter.Template)>
        │     ├╴<Context Python.string_format_expr at 171-178 (2 children)>
        │     │  ├╴<Token 'result' at 171:177 (Name.Variable)>
        │     │  ╰╴<Token '}' at 177:178 (Delimiter.Template)>
        │     ├╴<Token '.' at 178:179 (Literal.String)>
        │     ╰╴<Token '"' at 179:180 (Literal.String.End)>
        ╰╴<Token ')' at 180:181 (Delimiter)>


