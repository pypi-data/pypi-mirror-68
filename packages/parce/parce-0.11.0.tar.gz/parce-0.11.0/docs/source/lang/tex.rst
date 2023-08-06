tex
===

.. automodule:: parce.lang.tex
    :members:
    :undoc-members:
    :show-inheritance:

Example:
--------

Root lexicon ``Latex.root`` and text:

.. code-block:: tex

    % Latex example from wikipedia
    \documentclass[a4paper]{article}
    \usepackage[dutch]{babel}
    \begin{document}
    \section{Example paragraph}
    A formula follows:
    % a comment
    \[
    \pi = \sqrt{6\sum_{n=1}^{\infty}\frac{1}{n^2}}
       = \left(\int_{-\infty}^{+\infty}e^{-x^2}\,dx\right)^2
    \]
    \end{document} % End of document

Result tree::

    <Context Latex.root at 0-309 (24 children)>
     ├╴<Token '%' at 0:1 (Comment)>
     ├╴<Context Latex.comment at 1-30 (1 child)>
     │  ╰╴<Token ' Latex examp...rom wikipedia' at 1:30 (Comment)>
     ├╴<Token '\n' at 30:31 (Text)>
     ├╴<Token '\\documentclass' at 31:45 (Name.Command)>
     ├╴<Token '[' at 45:46 (Delimiter.Bracket)>
     ├╴<Context Latex.option at 46-54 (2 children)>
     │  ├╴<Token 'a4paper' at 46:53 (Pseudo)>
     │  ╰╴<Token ']' at 53:54 (Delimiter.Bracket)>
     ├╴<Token '{' at 54:55 (Delimiter.Brace)>
     ├╴<Context Latex.brace at 55-63 (2 children)>
     │  ├╴<Token 'article' at 55:62 (Text)>
     │  ╰╴<Token '}' at 62:63 (Delimiter.Brace)>
     ├╴<Token '\n' at 63:64 (Text)>
     ├╴<Token '\\usepackage' at 64:75 (Name.Command)>
     ├╴<Token '[' at 75:76 (Delimiter.Bracket)>
     ├╴<Context Latex.option at 76-82 (2 children)>
     │  ├╴<Token 'dutch' at 76:81 (Pseudo)>
     │  ╰╴<Token ']' at 81:82 (Delimiter.Bracket)>
     ├╴<Token '{' at 82:83 (Delimiter.Brace)>
     ├╴<Context Latex.brace at 83-89 (2 children)>
     │  ├╴<Token 'babel' at 83:88 (Text)>
     │  ╰╴<Token '}' at 88:89 (Delimiter.Brace)>
     ├╴<Token '\n' at 89:90 (Text)>
     ├╴<Token '\\begin' at 90:96 (Name.Builtin)>
     ├╴<Token '{' at 96:97 (Delimiter)>
     ├╴<Token 'document' at 97:105 (Name.Tag)>
     ├╴<Token '}' at 105:106 (Delimiter)>
     ├╴<Context Latex.environment at 106-290 (15 children)>
     │  ├╴<Token '\n' at 106:107 (Text)>
     │  ├╴<Token '\\section' at 107:115 (Name.Command)>
     │  ├╴<Token '{' at 115:116 (Delimiter.Brace)>
     │  ├╴<Context Latex.brace at 116-134 (2 children)>
     │  │  ├╴<Token 'Example paragraph' at 116:133 (Text)>
     │  │  ╰╴<Token '}' at 133:134 (Delimiter.Brace)>
     │  ├╴<Token '\nA formula follows:\n' at 134:154 (Text)>
     │  ├╴<Token '%' at 154:155 (Comment)>
     │  ├╴<Context Latex.comment at 155-165 (1 child)>
     │  │  ╰╴<Token ' a comment' at 155:165 (Comment)>
     │  ├╴<Token '\n' at 165:166 (Text)>
     │  ├╴<Token '\\[' at 166:168 (Delimiter)>
     │  ├╴<Context Latex.math* at 168-275 (32 children)>
     │  │  ├╴<Token '\n' at 168:169 (Text.Math)>
     │  │  ├╴<Token '\\pi' at 169:172 (Name.Function)>
     │  │  ├╴<Token ' ' at 172:173 (Text.Math)>
     │  │  ├╴<Token '=' at 173:174 (Delimiter.Operator)>
     │  │  ├╴<Token ' ' at 174:175 (Text.Math)>
     │  │  ├╴<Token '\\sqrt' at 175:180 (Name.Function)>
     │  │  ├╴<Token '{' at 180:181 (Delimiter.Brace)>
     │  │  ├╴<Context Latex.math at 181-215 (14 children)>
     │  │  │  ├╴<Token '6' at 181:182 (Literal.Number)>
     │  │  │  ├╴<Token '\\sum' at 182:186 (Name.Function)>
     │  │  │  ├╴<Token '_' at 186:187 (Name.Command)>
     │  │  │  ├╴<Token '{' at 187:188 (Delimiter.Brace)>
     │  │  │  ├╴<Context Latex.math at 188-192 (4 children)>
     │  │  │  │  ├╴<Token 'n' at 188:189 (Name.Variable)>
     │  │  │  │  ├╴<Token '=' at 189:190 (Delimiter.Operator)>
     │  │  │  │  ├╴<Token '1' at 190:191 (Literal.Number)>
     │  │  │  │  ╰╴<Token '}' at 191:192 (Delimiter)>
     │  │  │  ├╴<Token '^' at 192:193 (Name.Command)>
     │  │  │  ├╴<Token '{' at 193:194 (Delimiter.Brace)>
     │  │  │  ├╴<Context Latex.math at 194-201 (2 children)>
     │  │  │  │  ├╴<Token '\\infty' at 194:200 (Name.Function)>
     │  │  │  │  ╰╴<Token '}' at 200:201 (Delimiter)>
     │  │  │  ├╴<Token '\\frac' at 201:206 (Name.Function)>
     │  │  │  ├╴<Token '{' at 206:207 (Delimiter.Brace)>
     │  │  │  ├╴<Context Latex.math at 207-209 (2 children)>
     │  │  │  │  ├╴<Token '1' at 207:208 (Literal.Number)>
     │  │  │  │  ╰╴<Token '}' at 208:209 (Delimiter)>
     │  │  │  ├╴<Token '{' at 209:210 (Delimiter.Brace)>
     │  │  │  ├╴<Context Latex.math at 210-214 (4 children)>
     │  │  │  │  ├╴<Token 'n' at 210:211 (Name.Variable)>
     │  │  │  │  ├╴<Token '^' at 211:212 (Name.Command)>
     │  │  │  │  ├╴<Token '2' at 212:213 (Literal.Number)>
     │  │  │  │  ╰╴<Token '}' at 213:214 (Delimiter)>
     │  │  │  ╰╴<Token '}' at 214:215 (Delimiter)>
     │  │  ├╴<Token '\n   ' at 215:219 (Text.Math)>
     │  │  ├╴<Token '=' at 219:220 (Delimiter.Operator)>
     │  │  ├╴<Token ' ' at 220:221 (Text.Math)>
     │  │  ├╴<Token '\\left' at 221:226 (Name.Function)>
     │  │  ├╴<Token '(' at 226:227 (Delimiter)>
     │  │  ├╴<Token '\\int' at 227:231 (Name.Function)>
     │  │  ├╴<Token '_' at 231:232 (Name.Command)>
     │  │  ├╴<Token '{' at 232:233 (Delimiter.Brace)>
     │  │  ├╴<Context Latex.math at 233-241 (3 children)>
     │  │  │  ├╴<Token '-' at 233:234 (Delimiter.Operator)>
     │  │  │  ├╴<Token '\\infty' at 234:240 (Name.Function)>
     │  │  │  ╰╴<Token '}' at 240:241 (Delimiter)>
     │  │  ├╴<Token '^' at 241:242 (Name.Command)>
     │  │  ├╴<Token '{' at 242:243 (Delimiter.Brace)>
     │  │  ├╴<Context Latex.math at 243-251 (3 children)>
     │  │  │  ├╴<Token '+' at 243:244 (Delimiter.Operator)>
     │  │  │  ├╴<Token '\\infty' at 244:250 (Name.Function)>
     │  │  │  ╰╴<Token '}' at 250:251 (Delimiter)>
     │  │  ├╴<Token 'e' at 251:252 (Name.Variable)>
     │  │  ├╴<Token '^' at 252:253 (Name.Command)>
     │  │  ├╴<Token '{' at 253:254 (Delimiter.Brace)>
     │  │  ├╴<Context Latex.math at 254-259 (5 children)>
     │  │  │  ├╴<Token '-' at 254:255 (Delimiter.Operator)>
     │  │  │  ├╴<Token 'x' at 255:256 (Name.Variable)>
     │  │  │  ├╴<Token '^' at 256:257 (Name.Command)>
     │  │  │  ├╴<Token '2' at 257:258 (Literal.Number)>
     │  │  │  ╰╴<Token '}' at 258:259 (Delimiter)>
     │  │  ├╴<Token '\\,' at 259:261 (Text.Math)>
     │  │  ├╴<Token 'dx' at 261:263 (Name.Variable)>
     │  │  ├╴<Token '\\right' at 263:269 (Name.Function)>
     │  │  ├╴<Token ')' at 269:270 (Delimiter)>
     │  │  ├╴<Token '^' at 270:271 (Name.Command)>
     │  │  ├╴<Token '2' at 271:272 (Literal.Number)>
     │  │  ├╴<Token '\n' at 272:273 (Text.Math)>
     │  │  ╰╴<Token '\\]' at 273:275 (Delimiter)>
     │  ├╴<Token '\n' at 275:276 (Text)>
     │  ├╴<Token '\\end' at 276:280 (Name.Builtin)>
     │  ├╴<Token '{' at 280:281 (Delimiter)>
     │  ├╴<Token 'document' at 281:289 (Name.Tag)>
     │  ╰╴<Token '}' at 289:290 (Delimiter)>
     ├╴<Token ' ' at 290:291 (Text)>
     ├╴<Token '%' at 291:292 (Comment)>
     ├╴<Context Latex.comment at 292-308 (1 child)>
     │  ╰╴<Token ' End of document' at 292:308 (Comment)>
     ╰╴<Token '\n' at 308:309 (Text)>


