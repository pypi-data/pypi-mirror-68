html
====

.. automodule:: parce.lang.html
    :members:
    :undoc-members:
    :show-inheritance:

Example:
--------

Root lexicon ``Html.root`` and text:

.. code-block:: html

    <!DOCTYPE html>
    <!-- html example -->
    <html xmlns="http://www.w3.org/1999/xhtml">
      <head>
        <meta charset="utf-8" />
        <style>
        h1 {
          font-size: 20px;
        }
        </style>
      </head>
      <body>
        <h1>Hello World!</h1>
        <p style="color: red;">red text</p>
      </body>
    </html>

Result tree::

    <Context Html.root at 0-286 (13 children)>
     ├╴<Token '<!' at 0:2 (Delimiter)>
     ├╴<Token 'DOCTYPE' at 2:9 (Keyword)>
     ├╴<Token 'html' at 10:14 (Name.Tag.Definition)>
     ├╴<Context Html.doctype at 14-15 (1 child)>
     │  ╰╴<Token '>' at 14:15 (Delimiter)>
     ├╴<Token '\n' at 15:16 (Whitespace)>
     ├╴<Token '<!--' at 16:20 (Comment.Start)>
     ├╴<Context Html.comment at 20-37 (2 children)>
     │  ├╴<Token ' html example ' at 20:34 (Comment)>
     │  ╰╴<Token '-->' at 34:37 (Comment.End)>
     ├╴<Token '\n' at 37:38 (Whitespace)>
     ├╴<Token '<' at 38:39 (Delimiter)>
     ├╴<Token 'html' at 39:43 (Name.Tag)>
     ├╴<Context Html.attrs at 44-81 (5 children)>
     │  ├╴<Token 'xmlns' at 44:49 (Name.Attribute)>
     │  ├╴<Token '=' at 49:50 (Delimiter.Operator)>
     │  ├╴<Token '"' at 50:51 (Literal.String.Double.Start)>
     │  ├╴<Context Html.dqstring at 51-80 (2 children)>
     │  │  ├╴<Token 'http://www.w3.org/1999/xhtml' at 51:79 (Literal.String.Double)>
     │  │  ╰╴<Token '"' at 79:80 (Literal.String.Double.End)>
     │  ╰╴<Token '>' at 80:81 (Delimiter)>
     ├╴<Context Html.tag at 81-285 (14 children)>
     │  ├╴<Token '\n  ' at 81:84 (Whitespace)>
     │  ├╴<Token '<' at 84:85 (Delimiter)>
     │  ├╴<Token 'head' at 85:89 (Name.Tag)>
     │  ├╴<Token '>' at 89:90 (Delimiter)>
     │  ├╴<Context Html.tag at 90-192 (13 children)>
     │  │  ├╴<Token '\n    ' at 90:95 (Whitespace)>
     │  │  ├╴<Token '<' at 95:96 (Delimiter)>
     │  │  ├╴<Token 'meta' at 96:100 (Name.Tag)>
     │  │  ├╴<Context Html.attrs* at 101-119 (5 children)>
     │  │  │  ├╴<Token 'charset' at 101:108 (Name.Attribute)>
     │  │  │  ├╴<Token '=' at 108:109 (Delimiter.Operator)>
     │  │  │  ├╴<Token '"' at 109:110 (Literal.String.Double.Start)>
     │  │  │  ├╴<Context Html.dqstring at 110-116 (2 children)>
     │  │  │  │  ├╴<Token 'utf-8' at 110:115 (Literal.String.Double)>
     │  │  │  │  ╰╴<Token '"' at 115:116 (Literal.String.Double.End)>
     │  │  │  ╰╴<Token '/>' at 117:119 (Delimiter)>
     │  │  ├╴<Token '\n    ' at 119:124 (Whitespace)>
     │  │  ├╴<Token '<' at 124:125 (Delimiter)>
     │  │  ├╴<Token 'style' at 125:130 (Name.Tag)>
     │  │  ├╴<Token '>' at 130:131 (Delimiter)>
     │  │  ├╴<Context Html.css_style_tag at 136-182 (5 children)>
     │  │  │  ├╴<Context Css.prelude at 136-140 (2 children)>
     │  │  │  │  ├╴<Context Css.selector at 136-138 (1 child)>
     │  │  │  │  │  ╰╴<Context Css.element_selector at 136-138 (1 child)>
     │  │  │  │  │     ╰╴<Token 'h1' at 136:138 (Name.Tag)>
     │  │  │  │  ╰╴<Token '{' at 139:140 (Delimiter.Bracket)>
     │  │  │  ├╴<Context Css.rule at 147-169 (2 children)>
     │  │  │  │  ├╴<Context Css.declaration at 147-163 (5 children)>
     │  │  │  │  │  ├╴<Context Css.property at 147-156 (1 child)>
     │  │  │  │  │  │  ╰╴<Token 'font-size' at 147:156 (Name.Property.Definition)>
     │  │  │  │  │  ├╴<Token ':' at 156:157 (Delimiter)>
     │  │  │  │  │  ├╴<Token '20' at 158:160 (Literal.Number)>
     │  │  │  │  │  ├╴<Context Css.unit at 160-162 (1 child)>
     │  │  │  │  │  │  ╰╴<Token 'px' at 160:162 (Name.Unit)>
     │  │  │  │  │  ╰╴<Token ';' at 162:163 (Delimiter)>
     │  │  │  │  ╰╴<Token '}' at 168:169 (Delimiter.Bracket)>
     │  │  │  ├╴<Token '</' at 174:176 (Delimiter)>
     │  │  │  ├╴<Token 'style' at 176:181 (Name.Tag)>
     │  │  │  ╰╴<Token '>' at 181:182 (Delimiter)>
     │  │  ├╴<Token '\n  ' at 182:185 (Whitespace)>
     │  │  ├╴<Token '</' at 185:187 (Delimiter)>
     │  │  ├╴<Token 'head' at 187:191 (Name.Tag)>
     │  │  ╰╴<Token '>' at 191:192 (Delimiter)>
     │  ├╴<Token '\n  ' at 192:195 (Whitespace)>
     │  ├╴<Token '<' at 195:196 (Delimiter)>
     │  ├╴<Token 'body' at 196:200 (Name.Tag)>
     │  ├╴<Token '>' at 200:201 (Delimiter)>
     │  ├╴<Context Html.tag at 201-277 (14 children)>
     │  │  ├╴<Token '\n    ' at 201:206 (Whitespace)>
     │  │  ├╴<Token '<' at 206:207 (Delimiter)>
     │  │  ├╴<Token 'h1' at 207:209 (Name.Tag)>
     │  │  ├╴<Token '>' at 209:210 (Delimiter)>
     │  │  ├╴<Context Html.tag at 210-227 (4 children)>
     │  │  │  ├╴<Token 'Hello World!' at 210:222 (Text)>
     │  │  │  ├╴<Token '</' at 222:224 (Delimiter)>
     │  │  │  ├╴<Token 'h1' at 224:226 (Name.Tag)>
     │  │  │  ╰╴<Token '>' at 226:227 (Delimiter)>
     │  │  ├╴<Token '\n    ' at 227:232 (Whitespace)>
     │  │  ├╴<Token '<' at 232:233 (Delimiter)>
     │  │  ├╴<Token 'p' at 233:234 (Name.Tag)>
     │  │  ├╴<Context Html.attrs at 235-255 (5 children)>
     │  │  │  ├╴<Token 'style' at 235:240 (Name.Attribute)>
     │  │  │  ├╴<Token '=' at 240:241 (Delimiter.Operator)>
     │  │  │  ├╴<Token '"' at 241:242 (Literal.String)>
     │  │  │  ├╴<Context Html.css_style_attribute at 242-254 (5 children)>
     │  │  │  │  ├╴<Token 'color' at 242:247 (Name.Property.Definition)>
     │  │  │  │  ├╴<Token ':' at 247:248 (Delimiter)>
     │  │  │  │  ├╴<Token 'red' at 249:252 (Literal.Color)>
     │  │  │  │  ├╴<Token ';' at 252:253 (Delimiter)>
     │  │  │  │  ╰╴<Token '"' at 253:254 (Literal.String)>
     │  │  │  ╰╴<Token '>' at 254:255 (Delimiter)>
     │  │  ├╴<Context Html.tag at 255-267 (4 children)>
     │  │  │  ├╴<Token 'red text' at 255:263 (Text)>
     │  │  │  ├╴<Token '</' at 263:265 (Delimiter)>
     │  │  │  ├╴<Token 'p' at 265:266 (Name.Tag)>
     │  │  │  ╰╴<Token '>' at 266:267 (Delimiter)>
     │  │  ├╴<Token '\n  ' at 267:270 (Whitespace)>
     │  │  ├╴<Token '</' at 270:272 (Delimiter)>
     │  │  ├╴<Token 'body' at 272:276 (Name.Tag)>
     │  │  ╰╴<Token '>' at 276:277 (Delimiter)>
     │  ├╴<Token '\n' at 277:278 (Whitespace)>
     │  ├╴<Token '</' at 278:280 (Delimiter)>
     │  ├╴<Token 'html' at 280:284 (Name.Tag)>
     │  ╰╴<Token '>' at 284:285 (Delimiter)>
     ╰╴<Token '\n' at 285:286 (Whitespace)>


