css
===

.. automodule:: parce.lang.css
    :members:
    :undoc-members:
    :show-inheritance:

Example:
--------

Root lexicon ``Css.root`` and text:

.. code-block:: css

    /* css example */
    h1.main {
        color: red;
        background: grey url(bla.png);
    }

Result tree::

    <Context Css.root at 0-80 (4 children)>
     ├╴<Token '/*' at 0:2 (Comment)>
     ├╴<Context Css.comment at 2-17 (2 children)>
     │  ├╴<Token ' css example ' at 2:15 (Comment)>
     │  ╰╴<Token '*/' at 15:17 (Comment)>
     ├╴<Context Css.prelude at 18-27 (2 children)>
     │  ├╴<Context Css.selector at 18-25 (3 children)>
     │  │  ├╴<Context Css.element_selector at 18-20 (1 child)>
     │  │  │  ╰╴<Token 'h1' at 18:20 (Name.Tag)>
     │  │  ├╴<Token '.' at 20:21 (Keyword)>
     │  │  ╰╴<Context Css.class_selector at 21-25 (1 child)>
     │  │     ╰╴<Token 'main' at 21:25 (Name.Class)>
     │  ╰╴<Token '{' at 26:27 (Delimiter.Bracket)>
     ╰╴<Context Css.rule at 32-80 (3 children)>
        ├╴<Context Css.declaration at 32-43 (4 children)>
        │  ├╴<Context Css.property at 32-37 (1 child)>
        │  │  ╰╴<Token 'color' at 32:37 (Name.Property.Definition)>
        │  ├╴<Token ':' at 37:38 (Delimiter)>
        │  ├╴<Context Css.identifier at 39-42 (1 child)>
        │  │  ╰╴<Token 'red' at 39:42 (Literal.Color)>
        │  ╰╴<Token ';' at 42:43 (Delimiter)>
        ├╴<Context Css.declaration at 48-78 (7 children)>
        │  ├╴<Context Css.property at 48-58 (1 child)>
        │  │  ╰╴<Token 'background' at 48:58 (Name.Property.Definition)>
        │  ├╴<Token ':' at 58:59 (Delimiter)>
        │  ├╴<Context Css.identifier at 60-64 (1 child)>
        │  │  ╰╴<Token 'grey' at 60:64 (Literal.Color)>
        │  ├╴<Token 'url' at 65:68 (Name)>
        │  ├╴<Token '(' at 68:69 (Delimiter)>
        │  ├╴<Context Css.url_function at 69-77 (2 children)>
        │  │  ├╴<Token 'bla.png' at 69:76 (Literal.Url)>
        │  │  ╰╴<Token ')' at 76:77 (Delimiter)>
        │  ╰╴<Token ';' at 77:78 (Delimiter)>
        ╰╴<Token '}' at 79:80 (Delimiter.Bracket)>


