json
====

.. automodule:: parce.lang.json
    :members:
    :undoc-members:
    :show-inheritance:

Example:
--------

Root lexicon ``Json.root`` and text:

.. code-block:: json

    {
      "comment": "JSON example",
      "title": "Frescobaldi",
      "background": "background.png",
      "icon-size": 80,
      "contents": [
        { "x": 449, "y": 320, "type": "link", "path": "/Applications"},
        { "x": 188, "y": 320, "type": "file", "path": "../dist/Frescobaldi.app"},
        { "x": 100, "y": 70, "type": "file", "path": "../README.txt" },
        { "x": 100, "y": 185, "type": "file", "path": "../ChangeLog.txt" },
        { "x": 540, "y": 70, "type": "file", "path": "../COPYING.txt" }
      ]
    }

Result tree::

    <Context Json.root at 0-485 (2 children)>
     ├╴<Token '{' at 0:1 (Delimiter)>
     ╰╴<Context Json.object at 4-485 (10 children)>
        ├╴<Context Json.key at 4-14 (3 children)>
        │  ├╴<Token '"' at 4:5 (Literal.String)>
        │  ├╴<Context Json.string at 5-13 (2 children)>
        │  │  ├╴<Token 'comment' at 5:12 (Literal.String)>
        │  │  ╰╴<Token '"' at 12:13 (Literal.String)>
        │  ╰╴<Token ':' at 13:14 (Delimiter)>
        ├╴<Context Json.value at 15-30 (3 children)>
        │  ├╴<Token '"' at 15:16 (Literal.String)>
        │  ├╴<Context Json.string at 16-29 (2 children)>
        │  │  ├╴<Token 'JSON example' at 16:28 (Literal.String)>
        │  │  ╰╴<Token '"' at 28:29 (Literal.String)>
        │  ╰╴<Token ',' at 29:30 (Delimiter)>
        ├╴<Context Json.key at 33-41 (3 children)>
        │  ├╴<Token '"' at 33:34 (Literal.String)>
        │  ├╴<Context Json.string at 34-40 (2 children)>
        │  │  ├╴<Token 'title' at 34:39 (Literal.String)>
        │  │  ╰╴<Token '"' at 39:40 (Literal.String)>
        │  ╰╴<Token ':' at 40:41 (Delimiter)>
        ├╴<Context Json.value at 42-56 (3 children)>
        │  ├╴<Token '"' at 42:43 (Literal.String)>
        │  ├╴<Context Json.string at 43-55 (2 children)>
        │  │  ├╴<Token 'Frescobaldi' at 43:54 (Literal.String)>
        │  │  ╰╴<Token '"' at 54:55 (Literal.String)>
        │  ╰╴<Token ',' at 55:56 (Delimiter)>
        ├╴<Context Json.key at 59-72 (3 children)>
        │  ├╴<Token '"' at 59:60 (Literal.String)>
        │  ├╴<Context Json.string at 60-71 (2 children)>
        │  │  ├╴<Token 'background' at 60:70 (Literal.String)>
        │  │  ╰╴<Token '"' at 70:71 (Literal.String)>
        │  ╰╴<Token ':' at 71:72 (Delimiter)>
        ├╴<Context Json.value at 73-90 (3 children)>
        │  ├╴<Token '"' at 73:74 (Literal.String)>
        │  ├╴<Context Json.string at 74-89 (2 children)>
        │  │  ├╴<Token 'background.png' at 74:88 (Literal.String)>
        │  │  ╰╴<Token '"' at 88:89 (Literal.String)>
        │  ╰╴<Token ',' at 89:90 (Delimiter)>
        ├╴<Context Json.key at 93-105 (3 children)>
        │  ├╴<Token '"' at 93:94 (Literal.String)>
        │  ├╴<Context Json.string at 94-104 (2 children)>
        │  │  ├╴<Token 'icon-size' at 94:103 (Literal.String)>
        │  │  ╰╴<Token '"' at 103:104 (Literal.String)>
        │  ╰╴<Token ':' at 104:105 (Delimiter)>
        ├╴<Context Json.value at 106-109 (2 children)>
        │  ├╴<Token '80' at 106:108 (Literal.Number)>
        │  ╰╴<Token ',' at 108:109 (Delimiter)>
        ├╴<Context Json.key at 112-123 (3 children)>
        │  ├╴<Token '"' at 112:113 (Literal.String)>
        │  ├╴<Context Json.string at 113-122 (2 children)>
        │  │  ├╴<Token 'contents' at 113:121 (Literal.String)>
        │  │  ╰╴<Token '"' at 121:122 (Literal.String)>
        │  ╰╴<Token ':' at 122:123 (Delimiter)>
        ╰╴<Context Json.value at 124-485 (3 children)>
           ├╴<Token '[' at 124:125 (Delimiter)>
           ├╴<Context Json.array at 130-483 (15 children)>
           │  ├╴<Token '{' at 130:131 (Delimiter)>
           │  ├╴<Context Json.object at 132-192 (8 children)>
           │  │  ├╴<Context Json.key at 132-136 (3 children)>
           │  │  │  ├╴<Token '"' at 132:133 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 133-135 (2 children)>
           │  │  │  │  ├╴<Token 'x' at 133:134 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 134:135 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 135:136 (Delimiter)>
           │  │  ├╴<Context Json.value at 137-141 (2 children)>
           │  │  │  ├╴<Token '449' at 137:140 (Literal.Number)>
           │  │  │  ╰╴<Token ',' at 140:141 (Delimiter)>
           │  │  ├╴<Context Json.key at 142-146 (3 children)>
           │  │  │  ├╴<Token '"' at 142:143 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 143-145 (2 children)>
           │  │  │  │  ├╴<Token 'y' at 143:144 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 144:145 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 145:146 (Delimiter)>
           │  │  ├╴<Context Json.value at 147-151 (2 children)>
           │  │  │  ├╴<Token '320' at 147:150 (Literal.Number)>
           │  │  │  ╰╴<Token ',' at 150:151 (Delimiter)>
           │  │  ├╴<Context Json.key at 152-159 (3 children)>
           │  │  │  ├╴<Token '"' at 152:153 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 153-158 (2 children)>
           │  │  │  │  ├╴<Token 'type' at 153:157 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 157:158 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 158:159 (Delimiter)>
           │  │  ├╴<Context Json.value at 160-167 (3 children)>
           │  │  │  ├╴<Token '"' at 160:161 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 161-166 (2 children)>
           │  │  │  │  ├╴<Token 'link' at 161:165 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 165:166 (Literal.String)>
           │  │  │  ╰╴<Token ',' at 166:167 (Delimiter)>
           │  │  ├╴<Context Json.key at 168-175 (3 children)>
           │  │  │  ├╴<Token '"' at 168:169 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 169-174 (2 children)>
           │  │  │  │  ├╴<Token 'path' at 169:173 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 173:174 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 174:175 (Delimiter)>
           │  │  ╰╴<Context Json.value at 176-192 (3 children)>
           │  │     ├╴<Token '"' at 176:177 (Literal.String)>
           │  │     ├╴<Context Json.string at 177-191 (2 children)>
           │  │     │  ├╴<Token '/Applications' at 177:190 (Literal.String)>
           │  │     │  ╰╴<Token '"' at 190:191 (Literal.String)>
           │  │     ╰╴<Token '}' at 191:192 (Delimiter)>
           │  ├╴<Token ',' at 192:193 (Delimiter)>
           │  ├╴<Token '{' at 198:199 (Delimiter)>
           │  ├╴<Context Json.object at 200-270 (8 children)>
           │  │  ├╴<Context Json.key at 200-204 (3 children)>
           │  │  │  ├╴<Token '"' at 200:201 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 201-203 (2 children)>
           │  │  │  │  ├╴<Token 'x' at 201:202 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 202:203 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 203:204 (Delimiter)>
           │  │  ├╴<Context Json.value at 205-209 (2 children)>
           │  │  │  ├╴<Token '188' at 205:208 (Literal.Number)>
           │  │  │  ╰╴<Token ',' at 208:209 (Delimiter)>
           │  │  ├╴<Context Json.key at 210-214 (3 children)>
           │  │  │  ├╴<Token '"' at 210:211 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 211-213 (2 children)>
           │  │  │  │  ├╴<Token 'y' at 211:212 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 212:213 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 213:214 (Delimiter)>
           │  │  ├╴<Context Json.value at 215-219 (2 children)>
           │  │  │  ├╴<Token '320' at 215:218 (Literal.Number)>
           │  │  │  ╰╴<Token ',' at 218:219 (Delimiter)>
           │  │  ├╴<Context Json.key at 220-227 (3 children)>
           │  │  │  ├╴<Token '"' at 220:221 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 221-226 (2 children)>
           │  │  │  │  ├╴<Token 'type' at 221:225 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 225:226 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 226:227 (Delimiter)>
           │  │  ├╴<Context Json.value at 228-235 (3 children)>
           │  │  │  ├╴<Token '"' at 228:229 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 229-234 (2 children)>
           │  │  │  │  ├╴<Token 'file' at 229:233 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 233:234 (Literal.String)>
           │  │  │  ╰╴<Token ',' at 234:235 (Delimiter)>
           │  │  ├╴<Context Json.key at 236-243 (3 children)>
           │  │  │  ├╴<Token '"' at 236:237 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 237-242 (2 children)>
           │  │  │  │  ├╴<Token 'path' at 237:241 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 241:242 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 242:243 (Delimiter)>
           │  │  ╰╴<Context Json.value at 244-270 (3 children)>
           │  │     ├╴<Token '"' at 244:245 (Literal.String)>
           │  │     ├╴<Context Json.string at 245-269 (2 children)>
           │  │     │  ├╴<Token '../dist/Frescobaldi.app' at 245:268 (Literal.String)>
           │  │     │  ╰╴<Token '"' at 268:269 (Literal.String)>
           │  │     ╰╴<Token '}' at 269:270 (Delimiter)>
           │  ├╴<Token ',' at 270:271 (Delimiter)>
           │  ├╴<Token '{' at 276:277 (Delimiter)>
           │  ├╴<Context Json.object at 278-338 (8 children)>
           │  │  ├╴<Context Json.key at 278-282 (3 children)>
           │  │  │  ├╴<Token '"' at 278:279 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 279-281 (2 children)>
           │  │  │  │  ├╴<Token 'x' at 279:280 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 280:281 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 281:282 (Delimiter)>
           │  │  ├╴<Context Json.value at 283-287 (2 children)>
           │  │  │  ├╴<Token '100' at 283:286 (Literal.Number)>
           │  │  │  ╰╴<Token ',' at 286:287 (Delimiter)>
           │  │  ├╴<Context Json.key at 288-292 (3 children)>
           │  │  │  ├╴<Token '"' at 288:289 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 289-291 (2 children)>
           │  │  │  │  ├╴<Token 'y' at 289:290 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 290:291 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 291:292 (Delimiter)>
           │  │  ├╴<Context Json.value at 293-296 (2 children)>
           │  │  │  ├╴<Token '70' at 293:295 (Literal.Number)>
           │  │  │  ╰╴<Token ',' at 295:296 (Delimiter)>
           │  │  ├╴<Context Json.key at 297-304 (3 children)>
           │  │  │  ├╴<Token '"' at 297:298 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 298-303 (2 children)>
           │  │  │  │  ├╴<Token 'type' at 298:302 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 302:303 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 303:304 (Delimiter)>
           │  │  ├╴<Context Json.value at 305-312 (3 children)>
           │  │  │  ├╴<Token '"' at 305:306 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 306-311 (2 children)>
           │  │  │  │  ├╴<Token 'file' at 306:310 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 310:311 (Literal.String)>
           │  │  │  ╰╴<Token ',' at 311:312 (Delimiter)>
           │  │  ├╴<Context Json.key at 313-320 (3 children)>
           │  │  │  ├╴<Token '"' at 313:314 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 314-319 (2 children)>
           │  │  │  │  ├╴<Token 'path' at 314:318 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 318:319 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 319:320 (Delimiter)>
           │  │  ╰╴<Context Json.value at 321-338 (3 children)>
           │  │     ├╴<Token '"' at 321:322 (Literal.String)>
           │  │     ├╴<Context Json.string at 322-336 (2 children)>
           │  │     │  ├╴<Token '../README.txt' at 322:335 (Literal.String)>
           │  │     │  ╰╴<Token '"' at 335:336 (Literal.String)>
           │  │     ╰╴<Token '}' at 337:338 (Delimiter)>
           │  ├╴<Token ',' at 338:339 (Delimiter)>
           │  ├╴<Token '{' at 344:345 (Delimiter)>
           │  ├╴<Context Json.object at 346-410 (8 children)>
           │  │  ├╴<Context Json.key at 346-350 (3 children)>
           │  │  │  ├╴<Token '"' at 346:347 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 347-349 (2 children)>
           │  │  │  │  ├╴<Token 'x' at 347:348 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 348:349 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 349:350 (Delimiter)>
           │  │  ├╴<Context Json.value at 351-355 (2 children)>
           │  │  │  ├╴<Token '100' at 351:354 (Literal.Number)>
           │  │  │  ╰╴<Token ',' at 354:355 (Delimiter)>
           │  │  ├╴<Context Json.key at 356-360 (3 children)>
           │  │  │  ├╴<Token '"' at 356:357 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 357-359 (2 children)>
           │  │  │  │  ├╴<Token 'y' at 357:358 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 358:359 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 359:360 (Delimiter)>
           │  │  ├╴<Context Json.value at 361-365 (2 children)>
           │  │  │  ├╴<Token '185' at 361:364 (Literal.Number)>
           │  │  │  ╰╴<Token ',' at 364:365 (Delimiter)>
           │  │  ├╴<Context Json.key at 366-373 (3 children)>
           │  │  │  ├╴<Token '"' at 366:367 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 367-372 (2 children)>
           │  │  │  │  ├╴<Token 'type' at 367:371 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 371:372 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 372:373 (Delimiter)>
           │  │  ├╴<Context Json.value at 374-381 (3 children)>
           │  │  │  ├╴<Token '"' at 374:375 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 375-380 (2 children)>
           │  │  │  │  ├╴<Token 'file' at 375:379 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 379:380 (Literal.String)>
           │  │  │  ╰╴<Token ',' at 380:381 (Delimiter)>
           │  │  ├╴<Context Json.key at 382-389 (3 children)>
           │  │  │  ├╴<Token '"' at 382:383 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 383-388 (2 children)>
           │  │  │  │  ├╴<Token 'path' at 383:387 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 387:388 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 388:389 (Delimiter)>
           │  │  ╰╴<Context Json.value at 390-410 (3 children)>
           │  │     ├╴<Token '"' at 390:391 (Literal.String)>
           │  │     ├╴<Context Json.string at 391-408 (2 children)>
           │  │     │  ├╴<Token '../ChangeLog.txt' at 391:407 (Literal.String)>
           │  │     │  ╰╴<Token '"' at 407:408 (Literal.String)>
           │  │     ╰╴<Token '}' at 409:410 (Delimiter)>
           │  ├╴<Token ',' at 410:411 (Delimiter)>
           │  ├╴<Token '{' at 416:417 (Delimiter)>
           │  ├╴<Context Json.object at 418-479 (8 children)>
           │  │  ├╴<Context Json.key at 418-422 (3 children)>
           │  │  │  ├╴<Token '"' at 418:419 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 419-421 (2 children)>
           │  │  │  │  ├╴<Token 'x' at 419:420 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 420:421 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 421:422 (Delimiter)>
           │  │  ├╴<Context Json.value at 423-427 (2 children)>
           │  │  │  ├╴<Token '540' at 423:426 (Literal.Number)>
           │  │  │  ╰╴<Token ',' at 426:427 (Delimiter)>
           │  │  ├╴<Context Json.key at 428-432 (3 children)>
           │  │  │  ├╴<Token '"' at 428:429 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 429-431 (2 children)>
           │  │  │  │  ├╴<Token 'y' at 429:430 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 430:431 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 431:432 (Delimiter)>
           │  │  ├╴<Context Json.value at 433-436 (2 children)>
           │  │  │  ├╴<Token '70' at 433:435 (Literal.Number)>
           │  │  │  ╰╴<Token ',' at 435:436 (Delimiter)>
           │  │  ├╴<Context Json.key at 437-444 (3 children)>
           │  │  │  ├╴<Token '"' at 437:438 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 438-443 (2 children)>
           │  │  │  │  ├╴<Token 'type' at 438:442 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 442:443 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 443:444 (Delimiter)>
           │  │  ├╴<Context Json.value at 445-452 (3 children)>
           │  │  │  ├╴<Token '"' at 445:446 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 446-451 (2 children)>
           │  │  │  │  ├╴<Token 'file' at 446:450 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 450:451 (Literal.String)>
           │  │  │  ╰╴<Token ',' at 451:452 (Delimiter)>
           │  │  ├╴<Context Json.key at 453-460 (3 children)>
           │  │  │  ├╴<Token '"' at 453:454 (Literal.String)>
           │  │  │  ├╴<Context Json.string at 454-459 (2 children)>
           │  │  │  │  ├╴<Token 'path' at 454:458 (Literal.String)>
           │  │  │  │  ╰╴<Token '"' at 458:459 (Literal.String)>
           │  │  │  ╰╴<Token ':' at 459:460 (Delimiter)>
           │  │  ╰╴<Context Json.value at 461-479 (3 children)>
           │  │     ├╴<Token '"' at 461:462 (Literal.String)>
           │  │     ├╴<Context Json.string at 462-477 (2 children)>
           │  │     │  ├╴<Token '../COPYING.txt' at 462:476 (Literal.String)>
           │  │     │  ╰╴<Token '"' at 476:477 (Literal.String)>
           │  │     ╰╴<Token '}' at 478:479 (Delimiter)>
           │  ╰╴<Token ']' at 482:483 (Delimiter)>
           ╰╴<Token '}' at 484:485 (Delimiter)>


