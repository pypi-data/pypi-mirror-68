texinfo
=======

.. automodule:: parce.lang.texinfo
    :members:
    :undoc-members:
    :show-inheritance:

Example:
--------

Root lexicon ``Texinfo.root`` and text:

.. code-block:: texinfo

    \input texinfo   @c -*-texinfo-*-
    @c Example texinfo file from the texinfo manual
    @c see https://www.gnu.org/software/texinfo/
    @comment %**start of header
    @include version.texi
    @settitle GNU Sample @value{VERSION}
    @syncodeindex pg cp
    @comment %**end of header
    @copying
    This manual is for GNU Sample (version @value{VERSION}, @value{UPDATED}),
    which is an example in the Texinfo documentation.
    
    Copyright @copyright{} 2016 Free Software Foundation, Inc.
    
    @quotation
    Permission is granted to copy, distribute and/or modify this document
    under the terms of the GNU Free Documentation License, Version 1.3 or
    any later version published by the Free Software Foundation.
    @end quotation
    @end copying
    
    @dircategory Texinfo documentation system
    @direntry
    * sample: (sample)Invoking sample.
    @end direntry
    
    @titlepage
    @title GNU Sample
    @subtitle for version @value{VERSION}, @value{UPDATED}
    @author A.U. Thor (@email{bug-sample@@gnu.org})
    @page
    @vskip 0pt plus 1filll
    @insertcopying
    @end titlepage

Result tree::

    <Context Texinfo.root at 0-988 (80 children)>
     ├╴<Token '\\input texinfo   ' at 0:17 (Text)>
     ├╴<Token '@c' at 17:19 (Comment)>
     ├╴<Context Texinfo.singleline_comment at 19-33 (1 child)>
     │  ╰╴<Token ' -*-texinfo-*-' at 19:33 (Comment)>
     ├╴<Token '\n' at 33:34 (Text)>
     ├╴<Token '@c' at 34:36 (Comment)>
     ├╴<Context Texinfo.singleline_comment at 36-81 (1 child)>
     │  ╰╴<Token ' Example tex...exinfo manual' at 36:81 (Comment)>
     ├╴<Token '\n' at 81:82 (Text)>
     ├╴<Token '@c' at 82:84 (Comment)>
     ├╴<Context Texinfo.singleline_comment at 84-126 (2 children)>
     │  ├╴<Token ' see ' at 84:89 (Comment)>
     │  ╰╴<Token 'https://www....ware/texinfo/' at 89:126 (Comment.Url)>
     ├╴<Token '\n' at 126:127 (Text)>
     ├╴<Token '@comment' at 127:135 (Comment)>
     ├╴<Context Texinfo.singleline_comment at 135-154 (1 child)>
     │  ╰╴<Token ' %**start of header' at 135:154 (Comment)>
     ├╴<Token '\n' at 154:155 (Text)>
     ├╴<Token '@include' at 155:163 (Name.Command)>
     ├╴<Token ' version.texi\n' at 163:177 (Text)>
     ├╴<Token '@settitle' at 177:186 (Name.Command)>
     ├╴<Token ' GNU Sample ' at 186:198 (Text)>
     ├╴<Token '@value' at 198:204 (Name.Function)>
     ├╴<Token '{' at 204:205 (Delimiter.Bracket.Start)>
     ├╴<Context Texinfo.brace at 205-213 (2 children)>
     │  ├╴<Token 'VERSION' at 205:212 (Text)>
     │  ╰╴<Token '}' at 212:213 (Delimiter.Bracket.End)>
     ├╴<Token '\n' at 213:214 (Text)>
     ├╴<Token '@syncodeindex' at 214:227 (Name.Command)>
     ├╴<Token ' pg cp\n' at 227:234 (Text)>
     ├╴<Token '@comment' at 234:242 (Comment)>
     ├╴<Context Texinfo.singleline_comment at 242-259 (1 child)>
     │  ╰╴<Token ' %**end of header' at 242:259 (Comment)>
     ├╴<Token '\n' at 259:260 (Text)>
     ├╴<Token '@copying' at 260:268 (Name.Command)>
     ├╴<Token '\nThis manua...ple (version ' at 268:308 (Text)>
     ├╴<Token '@value' at 308:314 (Name.Function)>
     ├╴<Token '{' at 314:315 (Delimiter.Bracket.Start)>
     ├╴<Context Texinfo.brace at 315-323 (2 children)>
     │  ├╴<Token 'VERSION' at 315:322 (Text)>
     │  ╰╴<Token '}' at 322:323 (Delimiter.Bracket.End)>
     ├╴<Token ', ' at 323:325 (Text)>
     ├╴<Token '@value' at 325:331 (Name.Function)>
     ├╴<Token '{' at 331:332 (Delimiter.Bracket.Start)>
     ├╴<Context Texinfo.brace at 332-340 (2 children)>
     │  ├╴<Token 'UPDATED' at 332:339 (Text)>
     │  ╰╴<Token '}' at 339:340 (Delimiter.Bracket.End)>
     ├╴<Token '),\nwhich is...n\nCopyright ' at 340:404 (Text)>
     ├╴<Token '@copyright' at 404:414 (Name.Symbol)>
     ├╴<Token '{' at 414:415 (Delimiter.Bracket.Start)>
     ├╴<Token '}' at 415:416 (Delimiter.Bracket.End)>
     ├╴<Token ' 2016 Free S...ion, Inc.\n\n' at 416:454 (Text)>
     ├╴<Token '@quotation' at 454:464 (Name.Command)>
     ├╴<Token '\nPermission...Foundation.\n' at 464:666 (Text)>
     ├╴<Token '@end' at 666:670 (Name.Command)>
     ├╴<Token ' quotation\n' at 670:681 (Text)>
     ├╴<Token '@end' at 681:685 (Name.Command)>
     ├╴<Token ' copying\n\n' at 685:695 (Text)>
     ├╴<Token '@dircategory' at 695:707 (Name.Command)>
     ├╴<Token ' Texinfo doc...tion system\n' at 707:737 (Text)>
     ├╴<Token '@direntry' at 737:746 (Name.Command)>
     ├╴<Token '\n* sample: ...ing sample.\n' at 746:782 (Text)>
     ├╴<Token '@end' at 782:786 (Name.Command)>
     ├╴<Token ' direntry\n\n' at 786:797 (Text)>
     ├╴<Token '@titlepage' at 797:807 (Name.Command)>
     ├╴<Token '\n' at 807:808 (Text)>
     ├╴<Token '@title' at 808:814 (Name.Command)>
     ├╴<Token ' GNU Sample\n' at 814:826 (Text)>
     ├╴<Token '@subtitle' at 826:835 (Name.Command)>
     ├╴<Token ' for version ' at 835:848 (Text)>
     ├╴<Token '@value' at 848:854 (Name.Function)>
     ├╴<Token '{' at 854:855 (Delimiter.Bracket.Start)>
     ├╴<Context Texinfo.brace at 855-863 (2 children)>
     │  ├╴<Token 'VERSION' at 855:862 (Text)>
     │  ╰╴<Token '}' at 862:863 (Delimiter.Bracket.End)>
     ├╴<Token ', ' at 863:865 (Text)>
     ├╴<Token '@value' at 865:871 (Name.Function)>
     ├╴<Token '{' at 871:872 (Delimiter.Bracket.Start)>
     ├╴<Context Texinfo.brace at 872-880 (2 children)>
     │  ├╴<Token 'UPDATED' at 872:879 (Text)>
     │  ╰╴<Token '}' at 879:880 (Delimiter.Bracket.End)>
     ├╴<Token '\n' at 880:881 (Text)>
     ├╴<Token '@author' at 881:888 (Name.Command)>
     ├╴<Token ' A.U. Thor (' at 888:900 (Text)>
     ├╴<Token '@email' at 900:906 (Name.Function)>
     ├╴<Token '{' at 906:907 (Delimiter.Bracket.Start)>
     ├╴<Context Texinfo.brace at 907-927 (4 children)>
     │  ├╴<Token 'bug-sample' at 907:917 (Text)>
     │  ├╴<Token '@@' at 917:919 (Escape)>
     │  ├╴<Token 'gnu.org' at 919:926 (Text)>
     │  ╰╴<Token '}' at 926:927 (Delimiter.Bracket.End)>
     ├╴<Token ')\n' at 927:929 (Text)>
     ├╴<Token '@page' at 929:934 (Name.Command)>
     ├╴<Token '\n' at 934:935 (Text)>
     ├╴<Token '@vskip' at 935:941 (Name.Command)>
     ├╴<Token ' 0pt plus 1filll\n' at 941:958 (Text)>
     ├╴<Token '@insertcopying' at 958:972 (Name.Command)>
     ├╴<Token '\n' at 972:973 (Text)>
     ├╴<Token '@end' at 973:977 (Name.Command)>
     ╰╴<Token ' titlepage\n' at 977:988 (Text)>


