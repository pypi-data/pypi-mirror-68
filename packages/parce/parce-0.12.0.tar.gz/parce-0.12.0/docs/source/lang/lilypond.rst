lilypond
========

.. automodule:: parce.lang.lilypond
    :members:
    :undoc-members:
    :show-inheritance:

Example:
--------

Root lexicon ``LilyPond.root`` and text:

.. code-block:: lilypond

    \relative c'' {
      \time 7/4
      d2 c4 b2 a | b c4 b( a) g2
    }
    \addlyrics {
      Join us now and share the soft -- ware
    }

Result tree::

    <Context LilyPond.root at 0-114 (8 children)>
     ├╴<Token '\\relative' at 0:9 (Name.Builtin)>
     ├╴<Token 'c' at 10:11 (Name.Pitch)>
     ├╴<Token "''" at 11:13 (Text.Music.Pitch.Octave)>
     ├╴<Token '{' at 14:15 (Delimiter.Bracket.Start)>
     ├╴<Context LilyPond.sequential at 18-58 (20 children)>
     │  ├╴<Token '\\time' at 18:23 (Name.Builtin)>
     │  ├╴<Token '7/4' at 24:27 (Literal.Number)>
     │  ├╴<Token 'd' at 30:31 (Text.Music.Pitch)>
     │  ├╴<Token '2' at 31:32 (Literal.Number.Duration)>
     │  ├╴<Token 'c' at 33:34 (Text.Music.Pitch)>
     │  ├╴<Token '4' at 34:35 (Literal.Number.Duration)>
     │  ├╴<Token 'b' at 36:37 (Text.Music.Pitch)>
     │  ├╴<Token '2' at 37:38 (Literal.Number.Duration)>
     │  ├╴<Token 'a' at 39:40 (Text.Music.Pitch)>
     │  ├╴<Token '|' at 41:42 (Delimiter.Separator.PipeSymbol)>
     │  ├╴<Token 'b' at 43:44 (Text.Music.Pitch)>
     │  ├╴<Token 'c' at 45:46 (Text.Music.Pitch)>
     │  ├╴<Token '4' at 46:47 (Literal.Number.Duration)>
     │  ├╴<Token 'b' at 48:49 (Text.Music.Pitch)>
     │  ├╴<Token '(' at 49:50 (Name.Symbol.Spanner.Slur)>
     │  ├╴<Token 'a' at 51:52 (Text.Music.Pitch)>
     │  ├╴<Token ')' at 52:53 (Name.Symbol.Spanner.Slur)>
     │  ├╴<Token 'g' at 54:55 (Text.Music.Pitch)>
     │  ├╴<Token '2' at 55:56 (Literal.Number.Duration)>
     │  ╰╴<Token '}' at 57:58 (Delimiter.Bracket.End)>
     ├╴<Token '\\addlyrics' at 59:69 (Keyword.Lyric)>
     ├╴<Token '{' at 70:71 (Delimiter.Bracket.Start)>
     ╰╴<Context LilyPond.lyricmode at 74-114 (10 children)>
        ├╴<Token 'Join' at 74:78 (Text.Lyric.LyricText)>
        ├╴<Token 'us' at 79:81 (Text.Lyric.LyricText)>
        ├╴<Token 'now' at 82:85 (Text.Lyric.LyricText)>
        ├╴<Token 'and' at 86:89 (Text.Lyric.LyricText)>
        ├╴<Token 'share' at 90:95 (Text.Lyric.LyricText)>
        ├╴<Token 'the' at 96:99 (Text.Lyric.LyricText)>
        ├╴<Token 'soft' at 100:104 (Text.Lyric.LyricText)>
        ├╴<Token '--' at 105:107 (Delimiter.Lyric.LyricHyphen)>
        ├╴<Token 'ware' at 108:112 (Text.Lyric.LyricText)>
        ╰╴<Token '}' at 113:114 (Delimiter.Bracket.End)>


