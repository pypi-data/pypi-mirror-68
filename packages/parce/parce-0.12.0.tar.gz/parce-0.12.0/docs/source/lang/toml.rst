toml
====

.. automodule:: parce.lang.toml
    :members:
    :undoc-members:
    :show-inheritance:

Example:
--------

Root lexicon ``Toml.root`` and text:

.. code-block:: toml

    # toml example from https://github.com/toml-lang/toml
    # This is a TOML document.
    
    title = "TOML Example"
    
    [owner]
    name = "Tom Preston-Werner"
    dob = 1979-05-27T07:32:00-08:00 # First class dates
    
    [database]
    server = "192.168.1.1"
    ports = [ 8001, 8001, 8002 ]
    connection_max = 5000
    enabled = true
    
    [servers]
    
      # Indentation (tabs and/or spaces) is allowed but not required
      [servers.alpha]
      ip = "10.0.0.1"
      dc = "eqdc10"
    
      [servers.beta]
      ip = "10.0.0.2"
      dc = "eqdc10"
    
    [clients]
    data = [ ["gamma", "delta"], [1, 2] ]
    
    # Line breaks are OK when inside arrays
    hosts = [
      "alpha",
      "omega"
    ]

Result tree::

    <Context Toml.root at 0-598 (47 children)>
     ├╴<Token '#' at 0:1 (Comment)>
     ├╴<Context Toml.comment at 1-53 (2 children)>
     │  ├╴<Token ' toml example from ' at 1:20 (Comment)>
     │  ╰╴<Token 'https://gith...oml-lang/toml' at 20:53 (Comment.Url)>
     ├╴<Token '#' at 54:55 (Comment)>
     ├╴<Context Toml.comment at 55-80 (1 child)>
     │  ╰╴<Token ' This is a TOML document.' at 55:80 (Comment)>
     ├╴<Context Toml.key at 82-89 (2 children)>
     │  ├╴<Token 'title' at 82:87 (Name.Variable)>
     │  ╰╴<Token '=' at 88:89 (Delimiter.Operator.Assignment)>
     ├╴<Context Toml.value at 90-104 (2 children)>
     │  ├╴<Token '"' at 90:91 (Literal.String)>
     │  ╰╴<Context Toml.string_basic at 91-104 (2 children)>
     │     ├╴<Token 'TOML Example' at 91:103 (Literal.String)>
     │     ╰╴<Token '"' at 103:104 (Literal.String)>
     ├╴<Token '[' at 106:107 (Delimiter.Bracket)>
     ├╴<Context Toml.table at 107-113 (2 children)>
     │  ├╴<Token 'owner' at 107:112 (Name.Variable)>
     │  ╰╴<Token ']' at 112:113 (Delimiter.Bracket)>
     ├╴<Context Toml.key at 114-120 (2 children)>
     │  ├╴<Token 'name' at 114:118 (Name.Variable)>
     │  ╰╴<Token '=' at 119:120 (Delimiter.Operator.Assignment)>
     ├╴<Context Toml.value at 121-141 (2 children)>
     │  ├╴<Token '"' at 121:122 (Literal.String)>
     │  ╰╴<Context Toml.string_basic at 122-141 (2 children)>
     │     ├╴<Token 'Tom Preston-Werner' at 122:140 (Literal.String)>
     │     ╰╴<Token '"' at 140:141 (Literal.String)>
     ├╴<Context Toml.key at 142-147 (2 children)>
     │  ├╴<Token 'dob' at 142:145 (Name.Variable)>
     │  ╰╴<Token '=' at 146:147 (Delimiter.Operator.Assignment)>
     ├╴<Context Toml.value at 148-175 (2 children)>
     │  ├╴<Token '1979-05-27T07:32:00-08:00' at 148:173 (Literal.Timestamp)>
     │  ╰╴<Token '#' at 174:175 (Comment)>
     ├╴<Context Toml.comment at 175-193 (1 child)>
     │  ╰╴<Token ' First class dates' at 175:193 (Comment)>
     ├╴<Token '[' at 195:196 (Delimiter.Bracket)>
     ├╴<Context Toml.table at 196-205 (2 children)>
     │  ├╴<Token 'database' at 196:204 (Name.Variable)>
     │  ╰╴<Token ']' at 204:205 (Delimiter.Bracket)>
     ├╴<Context Toml.key at 206-214 (2 children)>
     │  ├╴<Token 'server' at 206:212 (Name.Variable)>
     │  ╰╴<Token '=' at 213:214 (Delimiter.Operator.Assignment)>
     ├╴<Context Toml.value at 215-228 (2 children)>
     │  ├╴<Token '"' at 215:216 (Literal.String)>
     │  ╰╴<Context Toml.string_basic at 216-228 (2 children)>
     │     ├╴<Token '192.168.1.1' at 216:227 (Literal.String)>
     │     ╰╴<Token '"' at 227:228 (Literal.String)>
     ├╴<Context Toml.key at 229-236 (2 children)>
     │  ├╴<Token 'ports' at 229:234 (Name.Variable)>
     │  ╰╴<Token '=' at 235:236 (Delimiter.Operator.Assignment)>
     ├╴<Context Toml.value at 237-257 (2 children)>
     │  ├╴<Token '[' at 237:238 (Delimiter.Bracket)>
     │  ╰╴<Context Toml.array at 239-257 (6 children)>
     │     ├╴<Token '8001' at 239:243 (Literal.Number)>
     │     ├╴<Token ',' at 243:244 (Delimiter.Separator)>
     │     ├╴<Token '8001' at 245:249 (Literal.Number)>
     │     ├╴<Token ',' at 249:250 (Delimiter.Separator)>
     │     ├╴<Token '8002' at 251:255 (Literal.Number)>
     │     ╰╴<Token ']' at 256:257 (Delimiter.Bracket)>
     ├╴<Context Toml.key at 258-274 (2 children)>
     │  ├╴<Token 'connection_max' at 258:272 (Name.Variable)>
     │  ╰╴<Token '=' at 273:274 (Delimiter.Operator.Assignment)>
     ├╴<Context Toml.value at 275-279 (1 child)>
     │  ╰╴<Token '5000' at 275:279 (Literal.Number)>
     ├╴<Context Toml.key at 280-289 (2 children)>
     │  ├╴<Token 'enabled' at 280:287 (Name.Variable)>
     │  ╰╴<Token '=' at 288:289 (Delimiter.Operator.Assignment)>
     ├╴<Context Toml.value at 290-294 (1 child)>
     │  ╰╴<Token 'true' at 290:294 (Name.Constant)>
     ├╴<Token '[' at 296:297 (Delimiter.Bracket)>
     ├╴<Context Toml.table at 297-305 (2 children)>
     │  ├╴<Token 'servers' at 297:304 (Name.Variable)>
     │  ╰╴<Token ']' at 304:305 (Delimiter.Bracket)>
     ├╴<Token '#' at 309:310 (Comment)>
     ├╴<Context Toml.comment at 310-371 (1 child)>
     │  ╰╴<Token ' Indentation... not required' at 310:371 (Comment)>
     ├╴<Token '[' at 374:375 (Delimiter.Bracket)>
     ├╴<Context Toml.table at 375-389 (4 children)>
     │  ├╴<Token 'servers' at 375:382 (Name.Variable)>
     │  ├╴<Token '.' at 382:383 (Delimiter.Dot)>
     │  ├╴<Token 'alpha' at 383:388 (Name.Variable)>
     │  ╰╴<Token ']' at 388:389 (Delimiter.Bracket)>
     ├╴<Context Toml.key at 392-396 (2 children)>
     │  ├╴<Token 'ip' at 392:394 (Name.Variable)>
     │  ╰╴<Token '=' at 395:396 (Delimiter.Operator.Assignment)>
     ├╴<Context Toml.value at 397-407 (2 children)>
     │  ├╴<Token '"' at 397:398 (Literal.String)>
     │  ╰╴<Context Toml.string_basic at 398-407 (2 children)>
     │     ├╴<Token '10.0.0.1' at 398:406 (Literal.String)>
     │     ╰╴<Token '"' at 406:407 (Literal.String)>
     ├╴<Context Toml.key at 410-414 (2 children)>
     │  ├╴<Token 'dc' at 410:412 (Name.Variable)>
     │  ╰╴<Token '=' at 413:414 (Delimiter.Operator.Assignment)>
     ├╴<Context Toml.value at 415-423 (2 children)>
     │  ├╴<Token '"' at 415:416 (Literal.String)>
     │  ╰╴<Context Toml.string_basic at 416-423 (2 children)>
     │     ├╴<Token 'eqdc10' at 416:422 (Literal.String)>
     │     ╰╴<Token '"' at 422:423 (Literal.String)>
     ├╴<Token '[' at 427:428 (Delimiter.Bracket)>
     ├╴<Context Toml.table at 428-441 (4 children)>
     │  ├╴<Token 'servers' at 428:435 (Name.Variable)>
     │  ├╴<Token '.' at 435:436 (Delimiter.Dot)>
     │  ├╴<Token 'beta' at 436:440 (Name.Variable)>
     │  ╰╴<Token ']' at 440:441 (Delimiter.Bracket)>
     ├╴<Context Toml.key at 444-448 (2 children)>
     │  ├╴<Token 'ip' at 444:446 (Name.Variable)>
     │  ╰╴<Token '=' at 447:448 (Delimiter.Operator.Assignment)>
     ├╴<Context Toml.value at 449-459 (2 children)>
     │  ├╴<Token '"' at 449:450 (Literal.String)>
     │  ╰╴<Context Toml.string_basic at 450-459 (2 children)>
     │     ├╴<Token '10.0.0.2' at 450:458 (Literal.String)>
     │     ╰╴<Token '"' at 458:459 (Literal.String)>
     ├╴<Context Toml.key at 462-466 (2 children)>
     │  ├╴<Token 'dc' at 462:464 (Name.Variable)>
     │  ╰╴<Token '=' at 465:466 (Delimiter.Operator.Assignment)>
     ├╴<Context Toml.value at 467-475 (2 children)>
     │  ├╴<Token '"' at 467:468 (Literal.String)>
     │  ╰╴<Context Toml.string_basic at 468-475 (2 children)>
     │     ├╴<Token 'eqdc10' at 468:474 (Literal.String)>
     │     ╰╴<Token '"' at 474:475 (Literal.String)>
     ├╴<Token '[' at 477:478 (Delimiter.Bracket)>
     ├╴<Context Toml.table at 478-486 (2 children)>
     │  ├╴<Token 'clients' at 478:485 (Name.Variable)>
     │  ╰╴<Token ']' at 485:486 (Delimiter.Bracket)>
     ├╴<Context Toml.key at 487-493 (2 children)>
     │  ├╴<Token 'data' at 487:491 (Name.Variable)>
     │  ╰╴<Token '=' at 492:493 (Delimiter.Operator.Assignment)>
     ├╴<Context Toml.value at 494-524 (2 children)>
     │  ├╴<Token '[' at 494:495 (Delimiter.Bracket)>
     │  ╰╴<Context Toml.array at 496-524 (6 children)>
     │     ├╴<Token '[' at 496:497 (Delimiter.Bracket)>
     │     ├╴<Context Toml.array at 497-514 (6 children)>
     │     │  ├╴<Token '"' at 497:498 (Literal.String)>
     │     │  ├╴<Context Toml.string_basic at 498-504 (2 children)>
     │     │  │  ├╴<Token 'gamma' at 498:503 (Literal.String)>
     │     │  │  ╰╴<Token '"' at 503:504 (Literal.String)>
     │     │  ├╴<Token ',' at 504:505 (Delimiter.Separator)>
     │     │  ├╴<Token '"' at 506:507 (Literal.String)>
     │     │  ├╴<Context Toml.string_basic at 507-513 (2 children)>
     │     │  │  ├╴<Token 'delta' at 507:512 (Literal.String)>
     │     │  │  ╰╴<Token '"' at 512:513 (Literal.String)>
     │     │  ╰╴<Token ']' at 513:514 (Delimiter.Bracket)>
     │     ├╴<Token ',' at 514:515 (Delimiter.Separator)>
     │     ├╴<Token '[' at 516:517 (Delimiter.Bracket)>
     │     ├╴<Context Toml.array at 517-522 (4 children)>
     │     │  ├╴<Token '1' at 517:518 (Literal.Number)>
     │     │  ├╴<Token ',' at 518:519 (Delimiter.Separator)>
     │     │  ├╴<Token '2' at 520:521 (Literal.Number)>
     │     │  ╰╴<Token ']' at 521:522 (Delimiter.Bracket)>
     │     ╰╴<Token ']' at 523:524 (Delimiter.Bracket)>
     ├╴<Token '#' at 526:527 (Comment)>
     ├╴<Context Toml.comment at 527-565 (1 child)>
     │  ╰╴<Token ' Line breaks...inside arrays' at 527:565 (Comment)>
     ├╴<Context Toml.key at 566-573 (2 children)>
     │  ├╴<Token 'hosts' at 566:571 (Name.Variable)>
     │  ╰╴<Token '=' at 572:573 (Delimiter.Operator.Assignment)>
     ╰╴<Context Toml.value at 574-598 (2 children)>
        ├╴<Token '[' at 574:575 (Delimiter.Bracket)>
        ╰╴<Context Toml.array at 578-598 (6 children)>
           ├╴<Token '"' at 578:579 (Literal.String)>
           ├╴<Context Toml.string_basic at 579-585 (2 children)>
           │  ├╴<Token 'alpha' at 579:584 (Literal.String)>
           │  ╰╴<Token '"' at 584:585 (Literal.String)>
           ├╴<Token ',' at 585:586 (Delimiter.Separator)>
           ├╴<Token '"' at 589:590 (Literal.String)>
           ├╴<Context Toml.string_basic at 590-596 (2 children)>
           │  ├╴<Token 'omega' at 590:595 (Literal.String)>
           │  ╰╴<Token '"' at 595:596 (Literal.String)>
           ╰╴<Token ']' at 597:598 (Delimiter.Bracket)>


