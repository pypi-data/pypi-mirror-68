xml
===

.. automodule:: parce.lang.xml
    :members:
    :undoc-members:
    :show-inheritance:

Examples:
---------

Root lexicon ``Xml.root`` and text:

.. code-block:: xml

    <?xml version="1.0" encoding="ISO-8859-1"?>
    <!-- xml example -->
    <note type="urgent">
      <to>Tove</to>
      <from>Jani&eacute;</from>
      <heading>Reminder</heading>
      <body>Don't <em>forget me</em> this weekend!</body>
    </note>

Result tree::

    <Context Xml.root at 0-222 (12 children)>
     ├╴<Token '<?' at 0:2 (Delimiter.Bracket.Preprocessed.Start)>
     ├╴<Token 'xml' at 2:5 (Name.Tag.Preprocessed)>
     ├╴<Context Xml.processing_instruction at 5-43 (11 children)>
     │  ├╴<Token ' ' at 5:6 (Text.Preprocessed)>
     │  ├╴<Token 'version' at 6:13 (Name.Attribute)>
     │  ├╴<Token '=' at 13:14 (Delimiter.Operator)>
     │  ├╴<Token '"' at 14:15 (Literal.String.Double.Start)>
     │  ├╴<Context Xml.dqstring at 15-19 (2 children)>
     │  │  ├╴<Token '1.0' at 15:18 (Literal.String.Double)>
     │  │  ╰╴<Token '"' at 18:19 (Literal.String.Double.End)>
     │  ├╴<Token ' ' at 19:20 (Text.Preprocessed)>
     │  ├╴<Token 'encoding' at 20:28 (Name.Attribute)>
     │  ├╴<Token '=' at 28:29 (Delimiter.Operator)>
     │  ├╴<Token '"' at 29:30 (Literal.String.Double.Start)>
     │  ├╴<Context Xml.dqstring at 30-41 (2 children)>
     │  │  ├╴<Token 'ISO-8859-1' at 30:40 (Literal.String.Double)>
     │  │  ╰╴<Token '"' at 40:41 (Literal.String.Double.End)>
     │  ╰╴<Token '?>' at 41:43 (Delimiter.Bracket.Preprocessed.End)>
     ├╴<Token '\n' at 43:44 (Whitespace)>
     ├╴<Token '<!--' at 44:48 (Comment.Start)>
     ├╴<Context Xml.comment at 48-64 (2 children)>
     │  ├╴<Token ' xml example ' at 48:61 (Comment)>
     │  ╰╴<Token '-->' at 61:64 (Comment.End)>
     ├╴<Token '\n' at 64:65 (Whitespace)>
     ├╴<Token '<' at 65:66 (Delimiter)>
     ├╴<Token 'note' at 66:70 (Name.Tag)>
     ├╴<Context Xml.attrs at 71-85 (5 children)>
     │  ├╴<Token 'type' at 71:75 (Name.Attribute)>
     │  ├╴<Token '=' at 75:76 (Delimiter.Operator)>
     │  ├╴<Token '"' at 76:77 (Literal.String.Double.Start)>
     │  ├╴<Context Xml.dqstring at 77-84 (2 children)>
     │  │  ├╴<Token 'urgent' at 77:83 (Literal.String.Double)>
     │  │  ╰╴<Token '"' at 83:84 (Literal.String.Double.End)>
     │  ╰╴<Token '>' at 84:85 (Delimiter)>
     ├╴<Context Xml.tag at 85-221 (24 children)>
     │  ├╴<Token '\n  ' at 85:88 (Whitespace)>
     │  ├╴<Token '<' at 88:89 (Delimiter)>
     │  ├╴<Token 'to' at 89:91 (Name.Tag)>
     │  ├╴<Token '>' at 91:92 (Delimiter)>
     │  ├╴<Context Xml.tag at 92-101 (4 children)>
     │  │  ├╴<Token 'Tove' at 92:96 (Text)>
     │  │  ├╴<Token '</' at 96:98 (Delimiter)>
     │  │  ├╴<Token 'to' at 98:100 (Name.Tag)>
     │  │  ╰╴<Token '>' at 100:101 (Delimiter)>
     │  ├╴<Token '\n  ' at 101:104 (Whitespace)>
     │  ├╴<Token '<' at 104:105 (Delimiter)>
     │  ├╴<Token 'from' at 105:109 (Name.Tag)>
     │  ├╴<Token '>' at 109:110 (Delimiter)>
     │  ├╴<Context Xml.tag at 110-129 (5 children)>
     │  │  ├╴<Token 'Jani' at 110:114 (Text)>
     │  │  ├╴<Token '&eacute;' at 114:122 (Escape)>
     │  │  ├╴<Token '</' at 122:124 (Delimiter)>
     │  │  ├╴<Token 'from' at 124:128 (Name.Tag)>
     │  │  ╰╴<Token '>' at 128:129 (Delimiter)>
     │  ├╴<Token '\n  ' at 129:132 (Whitespace)>
     │  ├╴<Token '<' at 132:133 (Delimiter)>
     │  ├╴<Token 'heading' at 133:140 (Name.Tag)>
     │  ├╴<Token '>' at 140:141 (Delimiter)>
     │  ├╴<Context Xml.tag at 141-159 (4 children)>
     │  │  ├╴<Token 'Reminder' at 141:149 (Text)>
     │  │  ├╴<Token '</' at 149:151 (Delimiter)>
     │  │  ├╴<Token 'heading' at 151:158 (Name.Tag)>
     │  │  ╰╴<Token '>' at 158:159 (Delimiter)>
     │  ├╴<Token '\n  ' at 159:162 (Whitespace)>
     │  ├╴<Token '<' at 162:163 (Delimiter)>
     │  ├╴<Token 'body' at 163:167 (Name.Tag)>
     │  ├╴<Token '>' at 167:168 (Delimiter)>
     │  ├╴<Context Xml.tag at 168-213 (9 children)>
     │  │  ├╴<Token "Don't " at 168:174 (Text)>
     │  │  ├╴<Token '<' at 174:175 (Delimiter)>
     │  │  ├╴<Token 'em' at 175:177 (Name.Tag)>
     │  │  ├╴<Token '>' at 177:178 (Delimiter)>
     │  │  ├╴<Context Xml.tag at 178-192 (4 children)>
     │  │  │  ├╴<Token 'forget me' at 178:187 (Text)>
     │  │  │  ├╴<Token '</' at 187:189 (Delimiter)>
     │  │  │  ├╴<Token 'em' at 189:191 (Name.Tag)>
     │  │  │  ╰╴<Token '>' at 191:192 (Delimiter)>
     │  │  ├╴<Token ' this weekend!' at 192:206 (Text)>
     │  │  ├╴<Token '</' at 206:208 (Delimiter)>
     │  │  ├╴<Token 'body' at 208:212 (Name.Tag)>
     │  │  ╰╴<Token '>' at 212:213 (Delimiter)>
     │  ├╴<Token '\n' at 213:214 (Whitespace)>
     │  ├╴<Token '</' at 214:216 (Delimiter)>
     │  ├╴<Token 'note' at 216:220 (Name.Tag)>
     │  ╰╴<Token '>' at 220:221 (Delimiter)>
     ╰╴<Token '\n' at 221:222 (Whitespace)>




Root lexicon ``Dtd.root`` and text:

.. code-block:: xml

    <!-- example doctype definition (dtd) -->
    <!ELEMENT book (chapter)*>
    <!ELEMENT chapter ANY>
    <!ENTITY author "Wilbert Berendsen">
    <!ENTITY chapter1 SYSTEM "chapter1.xml">
    <!ATTLIST chapter
        number ID #REQUIRED
        author CDATA #REQUIRED
        lastmodified CDATA #IMPLIED
    >

Result tree::

    <Context Dtd.root at 0-272 (22 children)>
     ├╴<Token '<!--' at 0:4 (Comment.Start)>
     ├╴<Context Dtd.comment at 4-41 (2 children)>
     │  ├╴<Token ' example doc...nition (dtd) ' at 4:38 (Comment)>
     │  ╰╴<Token '-->' at 38:41 (Comment.End)>
     ├╴<Token '<!' at 42:44 (Delimiter)>
     ├╴<Token 'ELEMENT' at 44:51 (Keyword)>
     ├╴<Token 'book' at 52:56 (Name.Element.Definition)>
     ├╴<Context Dtd.element at 57-68 (4 children)>
     │  ├╴<Token '(' at 57:58 (Delimiter.Bracket)>
     │  ├╴<Context Dtd.element_contents at 58-66 (2 children)>
     │  │  ├╴<Token 'chapter' at 58:65 (Name.Element)>
     │  │  ╰╴<Token ')' at 65:66 (Delimiter.Bracket)>
     │  ├╴<Token '*' at 66:67 (Delimiter.Operator)>
     │  ╰╴<Token '>' at 67:68 (Delimiter)>
     ├╴<Token '<!' at 69:71 (Delimiter)>
     ├╴<Token 'ELEMENT' at 71:78 (Keyword)>
     ├╴<Token 'chapter' at 79:86 (Name.Element.Definition)>
     ├╴<Context Dtd.element at 87-91 (2 children)>
     │  ├╴<Token 'ANY' at 87:90 (Name.Keyword)>
     │  ╰╴<Token '>' at 90:91 (Delimiter)>
     ├╴<Token '<!' at 92:94 (Delimiter)>
     ├╴<Token 'ENTITY' at 94:100 (Keyword)>
     ├╴<Token 'author' at 101:107 (Name.Entity.Definition)>
     ├╴<Context Dtd.entity at 108-128 (3 children)>
     │  ├╴<Token '"' at 108:109 (Literal.String.Double.Start)>
     │  ├╴<Context Dtd.dqstring at 109-127 (2 children)>
     │  │  ├╴<Token 'Wilbert Berendsen' at 109:126 (Literal.String.Double)>
     │  │  ╰╴<Token '"' at 126:127 (Literal.String.Double.End)>
     │  ╰╴<Token '>' at 127:128 (Delimiter)>
     ├╴<Token '<!' at 129:131 (Delimiter)>
     ├╴<Token 'ENTITY' at 131:137 (Keyword)>
     ├╴<Token 'chapter1' at 138:146 (Name.Entity.Definition)>
     ├╴<Context Dtd.entity at 147-169 (4 children)>
     │  ├╴<Token 'SYSTEM' at 147:153 (Keyword)>
     │  ├╴<Token '"' at 154:155 (Literal.String.Double.Start)>
     │  ├╴<Context Dtd.dqstring at 155-168 (2 children)>
     │  │  ├╴<Token 'chapter1.xml' at 155:167 (Literal.String.Double)>
     │  │  ╰╴<Token '"' at 167:168 (Literal.String.Double.End)>
     │  ╰╴<Token '>' at 168:169 (Delimiter)>
     ├╴<Token '<!' at 170:172 (Delimiter)>
     ├╴<Token 'ATTLIST' at 172:179 (Keyword)>
     ├╴<Token 'chapter' at 180:187 (Name.Element.Definition)>
     ╰╴<Context Dtd.attlist at 192-272 (10 children)>
        ├╴<Token 'number' at 192:198 (Name.Attribute.Definition)>
        ├╴<Token 'ID' at 199:201 (Name.Type)>
        ├╴<Token '#REQUIRED' at 202:211 (Name.Builtin)>
        ├╴<Token 'author' at 216:222 (Name.Attribute.Definition)>
        ├╴<Token 'CDATA' at 223:228 (Name.Type)>
        ├╴<Token '#REQUIRED' at 229:238 (Name.Builtin)>
        ├╴<Token 'lastmodified' at 243:255 (Name.Attribute.Definition)>
        ├╴<Token 'CDATA' at 256:261 (Name.Type)>
        ├╴<Token '#IMPLIED' at 262:270 (Name.Builtin)>
        ╰╴<Token '>' at 271:272 (Delimiter)>


