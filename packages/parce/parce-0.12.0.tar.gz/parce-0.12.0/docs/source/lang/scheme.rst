scheme
======

.. automodule:: parce.lang.scheme
    :members:
    :undoc-members:
    :show-inheritance:

Example:
--------

Root lexicon ``Scheme.root`` and text:

.. code-block:: scheme

    ; scheme example
    ; convert to html entities
    (define (attribute-escape s)
      (string-substitute "\n" "&#10;"
        (string-substitute "\"" "&quot;"
          (string-substitute "&" "&amp;"
            s))))

Result tree::

    <Context Scheme.root at 0-194 (6 children)>
     ├╴<Token ';' at 0:1 (Comment)>
     ├╴<Context Scheme.singleline_comment at 1-16 (1 child)>
     │  ╰╴<Token ' scheme example' at 1:16 (Comment)>
     ├╴<Token ';' at 17:18 (Comment)>
     ├╴<Context Scheme.singleline_comment at 18-43 (1 child)>
     │  ╰╴<Token ' convert to html entities' at 18:43 (Comment)>
     ├╴<Token '(' at 44:45 (Delimiter.OpenParen)>
     ╰╴<Context Scheme.list at 45-194 (6 children)>
        ├╴<Token 'define' at 45:51 (Keyword)>
        ├╴<Token '(' at 52:53 (Delimiter.OpenParen)>
        ├╴<Context Scheme.list at 53-72 (3 children)>
        │  ├╴<Token 'attribute-escape' at 53:69 (Name)>
        │  ├╴<Token 's' at 70:71 (Name)>
        │  ╰╴<Token ')' at 71:72 (Delimiter.CloseParen)>
        ├╴<Token '(' at 75:76 (Delimiter.OpenParen)>
        ├╴<Context Scheme.list at 76-193 (8 children)>
        │  ├╴<Token 'string-substitute' at 76:93 (Name)>
        │  ├╴<Token '"' at 94:95 (Literal.String)>
        │  ├╴<Context Scheme.string at 95-98 (2 children)>
        │  │  ├╴<Token '\\n' at 95:97 (Literal.String)>
        │  │  ╰╴<Token '"' at 97:98 (Literal.String)>
        │  ├╴<Token '"' at 99:100 (Literal.String)>
        │  ├╴<Context Scheme.string at 100-106 (2 children)>
        │  │  ├╴<Token '&#10;' at 100:105 (Literal.String)>
        │  │  ╰╴<Token '"' at 105:106 (Literal.String)>
        │  ├╴<Token '(' at 111:112 (Delimiter.OpenParen)>
        │  ├╴<Context Scheme.list at 112-192 (8 children)>
        │  │  ├╴<Token 'string-substitute' at 112:129 (Name)>
        │  │  ├╴<Token '"' at 130:131 (Literal.String)>
        │  │  ├╴<Context Scheme.string at 131-134 (2 children)>
        │  │  │  ├╴<Token '\\"' at 131:133 (Literal.String.Escape)>
        │  │  │  ╰╴<Token '"' at 133:134 (Literal.String)>
        │  │  ├╴<Token '"' at 135:136 (Literal.String)>
        │  │  ├╴<Context Scheme.string at 136-143 (2 children)>
        │  │  │  ├╴<Token '&quot;' at 136:142 (Literal.String)>
        │  │  │  ╰╴<Token '"' at 142:143 (Literal.String)>
        │  │  ├╴<Token '(' at 150:151 (Delimiter.OpenParen)>
        │  │  ├╴<Context Scheme.list at 151-191 (7 children)>
        │  │  │  ├╴<Token 'string-substitute' at 151:168 (Name)>
        │  │  │  ├╴<Token '"' at 169:170 (Literal.String)>
        │  │  │  ├╴<Context Scheme.string at 170-172 (2 children)>
        │  │  │  │  ├╴<Token '&' at 170:171 (Literal.String)>
        │  │  │  │  ╰╴<Token '"' at 171:172 (Literal.String)>
        │  │  │  ├╴<Token '"' at 173:174 (Literal.String)>
        │  │  │  ├╴<Context Scheme.string at 174-180 (2 children)>
        │  │  │  │  ├╴<Token '&amp;' at 174:179 (Literal.String)>
        │  │  │  │  ╰╴<Token '"' at 179:180 (Literal.String)>
        │  │  │  ├╴<Token 's' at 189:190 (Name)>
        │  │  │  ╰╴<Token ')' at 190:191 (Delimiter.CloseParen)>
        │  │  ╰╴<Token ')' at 191:192 (Delimiter.CloseParen)>
        │  ╰╴<Token ')' at 192:193 (Delimiter.CloseParen)>
        ╰╴<Token ')' at 193:194 (Delimiter.CloseParen)>


