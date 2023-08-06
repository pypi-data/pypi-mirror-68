javascript
==========

.. automodule:: parce.lang.javascript
    :members:
    :undoc-members:
    :show-inheritance:

Example:
--------

Root lexicon ``JavaScript.root`` and text:

.. code-block:: javascript

    /*
     * small javascript example
     */
    
    var a = [100];
    var b = /a\reg\\[exp]/i;
    function c() {
        obj.meth(234);
        a[0] = "abc123";
    }
    

Result tree::

    <Context JavaScript.root at 0-132 (19 children)>
     ├╴<Token '/*' at 0:2 (Comment.Start)>
     ├╴<Context JavaScript.multiline_comment at 2-34 (2 children)>
     │  ├╴<Token '\n * small j...pt example\n ' at 2:32 (Comment)>
     │  ╰╴<Token '*/' at 32:34 (Comment.End)>
     ├╴<Token 'var' at 36:39 (Keyword)>
     ├╴<Token 'a' at 40:41 (Name.Variable.Definition)>
     ├╴<Token '=' at 42:43 (Delimiter.Operator.Assignment)>
     ├╴<Token '[' at 44:45 (Delimiter.Bracket.Start)>
     ├╴<Context JavaScript.array at 45-49 (2 children)>
     │  ├╴<Token '100' at 45:48 (Literal.Number)>
     │  ╰╴<Token ']' at 48:49 (Delimiter.Bracket.End)>
     ├╴<Token ';' at 49:50 (Delimiter)>
     ├╴<Token 'var' at 51:54 (Keyword)>
     ├╴<Token 'b' at 55:56 (Name.Variable.Definition)>
     ├╴<Token '=' at 57:58 (Delimiter.Operator.Assignment)>
     ├╴<Token '/a\\reg\\\\[exp]/i' at 59:74 (Literal.Regexp)>
     ├╴<Token ';' at 74:75 (Delimiter)>
     ├╴<Token 'function' at 76:84 (Keyword)>
     ├╴<Token 'c' at 85:86 (Name.Function.Definition)>
     ├╴<Token '(' at 86:87 (Delimiter)>
     ├╴<Context JavaScript.paren at 87-88 (1 child)>
     │  ╰╴<Token ')' at 87:88 (Delimiter)>
     ├╴<Token '{' at 89:90 (Delimiter.Bracket.Start)>
     ╰╴<Context JavaScript.scope at 95-132 (14 children)>
        ├╴<Token 'obj' at 95:98 (Name.Variable)>
        ├╴<Token '.' at 98:99 (Delimiter)>
        ├╴<Token 'meth' at 99:103 (Name.Method)>
        ├╴<Token '(' at 103:104 (Delimiter)>
        ├╴<Context JavaScript.call at 104-108 (2 children)>
        │  ├╴<Token '234' at 104:107 (Literal.Number)>
        │  ╰╴<Token ')' at 107:108 (Delimiter)>
        ├╴<Token ';' at 108:109 (Delimiter)>
        ├╴<Token 'a' at 114:115 (Name.Variable)>
        ├╴<Token '[' at 115:116 (Delimiter)>
        ├╴<Context JavaScript.index at 116-118 (2 children)>
        │  ├╴<Token '0' at 116:117 (Literal.Number)>
        │  ╰╴<Token ']' at 117:118 (Delimiter)>
        ├╴<Token '=' at 119:120 (Delimiter.Operator.Assignment)>
        ├╴<Token '"' at 121:122 (Literal.String.Start)>
        ├╴<Context JavaScript.string* at 122-129 (2 children)>
        │  ├╴<Token 'abc123' at 122:128 (Literal.String)>
        │  ╰╴<Token '"' at 128:129 (Literal.String.End)>
        ├╴<Token ';' at 129:130 (Delimiter)>
        ╰╴<Token '}' at 131:132 (Delimiter.Bracket.End)>


