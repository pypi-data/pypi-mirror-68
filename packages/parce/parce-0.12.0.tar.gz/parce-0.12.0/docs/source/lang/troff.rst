troff
=====

.. automodule:: parce.lang.troff
    :members:
    :undoc-members:
    :show-inheritance:

Example:
--------

Root lexicon ``Troff.root`` and text:

.. code-block:: troff

    .\" This is a comment
    .TH APPLICATION 1 "May 2020" "Description"
    .SH NAME
    my_application
    \- Short Description
    .SH SYNOPSIS
    my_application [options] files
    .SH DESCRIPTION
    Short Description
    .SH OPTIONS
    .SS
    .SS Arguments:
    .TP
    .B files
    Files to open, may also be URLs
    .SS Options:
    .TP
    .B \-v,  \-\-version
    Show version information
    
    This is some \fBbold\fR text.

Result tree::

    <Context Troff.root at 0-358 (37 children)>
     ├╴<Token '.' at 0:1 (Delimiter.Request)>
     ├╴<Context Troff.request at 1-21 (2 children)>
     │  ├╴<Token '\\"' at 1:3 (Comment)>
     │  ╰╴<Context Troff.comment at 3-21 (1 child)>
     │     ╰╴<Token ' This is a comment' at 3:21 (Comment)>
     ├╴<Token '.' at 22:23 (Delimiter.Request)>
     ├╴<Context Troff.request at 23-64 (7 children)>
     │  ├╴<Context Troff.name at 23-25 (1 child)>
     │  │  ╰╴<Token 'TH' at 23:25 (Name.Identifier)>
     │  ├╴<Token ' APPLICATION ' at 25:38 (Text)>
     │  ├╴<Token '1' at 38:39 (Literal.Number)>
     │  ├╴<Token '"' at 40:41 (Literal.String)>
     │  ├╴<Context Troff.string at 41-50 (2 children)>
     │  │  ├╴<Token 'May 2020' at 41:49 (Literal.String)>
     │  │  ╰╴<Token '"' at 49:50 (Literal.String)>
     │  ├╴<Token '"' at 51:52 (Literal.String)>
     │  ╰╴<Context Troff.string at 52-64 (2 children)>
     │     ├╴<Token 'Description' at 52:63 (Literal.String)>
     │     ╰╴<Token '"' at 63:64 (Literal.String)>
     ├╴<Token '.' at 65:66 (Delimiter.Request)>
     ├╴<Context Troff.request at 66-73 (2 children)>
     │  ├╴<Context Troff.name at 66-68 (1 child)>
     │  │  ╰╴<Token 'SH' at 66:68 (Name.Identifier)>
     │  ╰╴<Token ' NAME' at 68:73 (Text)>
     ├╴<Token 'my_application\n' at 74:89 (Text)>
     ├╴<Token '\\-' at 89:91 (Text.Escape)>
     ├╴<Token ' Short Description\n' at 91:110 (Text)>
     ├╴<Token '.' at 110:111 (Delimiter.Request)>
     ├╴<Context Troff.request at 111-122 (2 children)>
     │  ├╴<Context Troff.name at 111-113 (1 child)>
     │  │  ╰╴<Token 'SH' at 111:113 (Name.Identifier)>
     │  ╰╴<Token ' SYNOPSIS' at 113:122 (Text)>
     ├╴<Token 'my_applicati...ions] files\n' at 123:154 (Text)>
     ├╴<Token '.' at 154:155 (Delimiter.Request)>
     ├╴<Context Troff.request at 155-169 (2 children)>
     │  ├╴<Context Troff.name at 155-157 (1 child)>
     │  │  ╰╴<Token 'SH' at 155:157 (Name.Identifier)>
     │  ╰╴<Token ' DESCRIPTION' at 157:169 (Text)>
     ├╴<Token 'Short Description\n' at 170:188 (Text)>
     ├╴<Token '.' at 188:189 (Delimiter.Request)>
     ├╴<Context Troff.request at 189-199 (2 children)>
     │  ├╴<Context Troff.name at 189-191 (1 child)>
     │  │  ╰╴<Token 'SH' at 189:191 (Name.Identifier)>
     │  ╰╴<Token ' OPTIONS' at 191:199 (Text)>
     ├╴<Token '.' at 200:201 (Delimiter.Request)>
     ├╴<Context Troff.request at 201-203 (1 child)>
     │  ╰╴<Context Troff.name at 201-203 (1 child)>
     │     ╰╴<Token 'SS' at 201:203 (Name.Identifier)>
     ├╴<Token '.' at 204:205 (Delimiter.Request)>
     ├╴<Context Troff.request at 205-218 (3 children)>
     │  ├╴<Context Troff.name at 205-207 (1 child)>
     │  │  ╰╴<Token 'SS' at 205:207 (Name.Identifier)>
     │  ├╴<Token ' Arguments' at 207:217 (Text)>
     │  ╰╴<Token ':' at 217:218 (Delimiter.Operator)>
     ├╴<Token '.' at 219:220 (Delimiter.Request)>
     ├╴<Context Troff.request at 220-222 (1 child)>
     │  ╰╴<Context Troff.name at 220-222 (1 child)>
     │     ╰╴<Token 'TP' at 220:222 (Name.Identifier)>
     ├╴<Token '.' at 223:224 (Delimiter.Request)>
     ├╴<Context Troff.request at 224-231 (2 children)>
     │  ├╴<Context Troff.name at 224-225 (1 child)>
     │  │  ╰╴<Token 'B' at 224:225 (Name.Identifier)>
     │  ╰╴<Token ' files' at 225:231 (Text)>
     ├╴<Token 'Files to ope...lso be URLs\n' at 232:264 (Text)>
     ├╴<Token '.' at 264:265 (Delimiter.Request)>
     ├╴<Context Troff.request at 265-276 (3 children)>
     │  ├╴<Context Troff.name at 265-267 (1 child)>
     │  │  ╰╴<Token 'SS' at 265:267 (Name.Identifier)>
     │  ├╴<Token ' Options' at 267:275 (Text)>
     │  ╰╴<Token ':' at 275:276 (Delimiter.Operator)>
     ├╴<Token '.' at 277:278 (Delimiter.Request)>
     ├╴<Context Troff.request at 278-280 (1 child)>
     │  ╰╴<Context Troff.name at 278-280 (1 child)>
     │     ╰╴<Token 'TP' at 278:280 (Name.Identifier)>
     ├╴<Token '.' at 281:282 (Delimiter.Request)>
     ├╴<Context Troff.request at 282-301 (7 children)>
     │  ├╴<Context Troff.name at 282-283 (1 child)>
     │  │  ╰╴<Token 'B' at 282:283 (Name.Identifier)>
     │  ├╴<Token ' ' at 283:284 (Text)>
     │  ├╴<Token '\\-' at 284:286 (Text.Escape)>
     │  ├╴<Token 'v,  ' at 286:290 (Text)>
     │  ├╴<Token '\\-' at 290:292 (Text.Escape)>
     │  ├╴<Token '\\-' at 292:294 (Text.Escape)>
     │  ╰╴<Token 'version' at 294:301 (Text)>
     ├╴<Token 'Show version...This is some ' at 302:341 (Text)>
     ├╴<Token '\\fB' at 341:344 (Text.Escape)>
     ├╴<Token 'bold' at 344:348 (Text)>
     ├╴<Token '\\fR' at 348:351 (Text.Escape)>
     ╰╴<Token ' text.\n' at 351:358 (Text)>


