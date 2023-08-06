ini
===

.. automodule:: parce.lang.ini
    :members:
    :undoc-members:
    :show-inheritance:

Example:
--------

Root lexicon ``Ini.root`` and text:

.. code-block:: ini

    ; ini example
    ; last modified 1 April 2001 by John Doe
    [owner]
    name=John Doe
    organization=Acme Widgets Inc.
    
    [database]
    ; use IP address in case network name resolution is not working
    server=192.0.2.62
    port=143
    file="payroll.dat"

Result tree::

    <Context Ini.root at 0-229 (25 children)>
     ├╴<Token ';' at 0:1 (Comment)>
     ├╴<Context Ini.comment at 1-13 (1 child)>
     │  ╰╴<Token ' ini example' at 1:13 (Comment)>
     ├╴<Token ';' at 14:15 (Comment)>
     ├╴<Context Ini.comment at 15-54 (1 child)>
     │  ╰╴<Token ' last modifi...1 by John Doe' at 15:54 (Comment)>
     ├╴<Token '[' at 55:56 (Delimiter.Section)>
     ├╴<Context Ini.section at 56-62 (2 children)>
     │  ├╴<Token 'owner' at 56:61 (Name.Namespace.Section)>
     │  ╰╴<Token ']' at 61:62 (Delimiter.Section)>
     ├╴<Context Ini.key at 63-67 (1 child)>
     │  ╰╴<Token 'name' at 63:67 (Name.Identifier)>
     ├╴<Token '=' at 67:68 (Delimiter.Operator.Assignment)>
     ├╴<Context Ini.value at 68-76 (1 child)>
     │  ╰╴<Token 'John Doe' at 68:76 (Literal.Data)>
     ├╴<Context Ini.key at 77-89 (1 child)>
     │  ╰╴<Token 'organization' at 77:89 (Name.Identifier)>
     ├╴<Token '=' at 89:90 (Delimiter.Operator.Assignment)>
     ├╴<Context Ini.value at 90-107 (1 child)>
     │  ╰╴<Token 'Acme Widgets Inc.' at 90:107 (Literal.Data)>
     ├╴<Token '[' at 109:110 (Delimiter.Section)>
     ├╴<Context Ini.section at 110-119 (2 children)>
     │  ├╴<Token 'database' at 110:118 (Name.Namespace.Section)>
     │  ╰╴<Token ']' at 118:119 (Delimiter.Section)>
     ├╴<Token ';' at 120:121 (Comment)>
     ├╴<Context Ini.comment at 121-183 (1 child)>
     │  ╰╴<Token ' use IP addr...s not working' at 121:183 (Comment)>
     ├╴<Context Ini.key at 184-190 (1 child)>
     │  ╰╴<Token 'server' at 184:190 (Name.Identifier)>
     ├╴<Token '=' at 190:191 (Delimiter.Operator.Assignment)>
     ├╴<Context Ini.value at 191-201 (1 child)>
     │  ╰╴<Token '192.0.2.62' at 191:201 (Literal.Data)>
     ├╴<Context Ini.key at 202-206 (1 child)>
     │  ╰╴<Token 'port' at 202:206 (Name.Identifier)>
     ├╴<Token '=' at 206:207 (Delimiter.Operator.Assignment)>
     ├╴<Context Ini.value at 207-210 (1 child)>
     │  ╰╴<Token '143' at 207:210 (Literal.Data)>
     ├╴<Context Ini.key at 211-215 (1 child)>
     │  ╰╴<Token 'file' at 211:215 (Name.Identifier)>
     ├╴<Token '=' at 215:216 (Delimiter.Operator.Assignment)>
     ╰╴<Context Ini.value at 216-229 (1 child)>
        ╰╴<Token '"payroll.dat"' at 216:229 (Literal.Data)>


