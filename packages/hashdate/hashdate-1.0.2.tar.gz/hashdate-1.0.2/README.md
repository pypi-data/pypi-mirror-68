![hashdate](https://github.com/sloev/hashdate/blob/master/assets/logo.png)

# HashDate 

[![Latest Version](https://img.shields.io/pypi/v/hashdate.svg)](https://pypi.python.org/pypi/hashdate) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Turns Python datetimes (or iso dates with `cli`) into hashes.

The hashes support shortening to reduce precision, so a prefix of a hash will be the same datetime rounded to the given hashlength.

## Cli usage

Check out the demo:
```bash
$ hashdate demo
``` 

Its full of colors:

[![asciicast](https://asciinema.org/a/kKaOD68BJXa11WA1ghW7vjqii.svg)](https://asciinema.org/a/kKaOD68BJXa11WA1ghW7vjqii)

Turn your iso date into a hash:

```bash
$ hashdate date2hash 2020-05-13T22:30:47.136450
hash: UCABCBDCCDAEHBDGEFA
```

Then if you only take the first 11 chars you get a datetime with less precision:

```bash
$ hashdate hash2date UCABCBDCCDA
datetime: 2020-05-13T22:30:00
```

you can also secify to use emojis for charset if you want to:

```bash
$ hashdate date2hash 2020-05-13T22:30:47.136450 -c emoji
hash: 🌹🐲🌼🥕🐲🥕🌲🐲🐲🌲🌼🍇🐐🥕🌲🌴🍇🐂🌼
```

and back again:

```bash
$ hash2date 🌹🐲🌼🥕🐲🥕🌲🐲🐲🌲🌼🍇🐐🥕🌲🌴🍇🐂🌼 -c emoji
datetime: 2020-05-13T22:30:47.136450
```

## Module usage

```python
import datetime
from hashdate import datetime_to_hash, hash_to_datetime

now = datetime.datetime.now()
hash = datetime_to_hash(now)
dt = hash_to_datetime(hash)
assert now == dt
```

### Advanced

Use emojis:

```python
import datetime
from hashdate import datetime_to_hash, hash_to_datetime

now = datetime.datetime.now()
hash = datetime_to_hash(now, charset='emoji')
dt = hash_to_datetime(hash, charset='emoji')
assert now == dt
```

Register more charsets:

```python
import datetime
from hashdate import register_charset, datetime_to_hash, hash_to_datetime

charset = "🌼🥕🐲🌲🍇🐂🌴🐐🍉🌺🍊🐽🍆🦎🍟🌱🐫🐍🐃🍍🌹🍕☘🌿🥓🐪🌷🏵🔥🐷🌳🌶🥒🐊🐗🐏🌵🌻🌽🐢🍋🍈💮🎃🌊🥔🌰🍀🍃💧💐🍂🐮🌸🐄🍄🍁🍞🥜🐑🥀🌭🐸🐖"

register_charset('my_emojis', charset)

now = datetime.datetime.now()
hash = datetime_to_hash(now, charset='my_emojis')
dt = hash_to_datetime(hash, charset='my_emojis')
assert now == dt
```


## Structure of a hashdate

```
centenial: [...19,20,21...]
|    quarter start month: [0,3,6,9]
|    |   day in tens: [0:3]
|    |   |   hour in tens: [0:5]
|    |   |   |   minute in tens: [0:5]
|    |   |   |   |   second in tens: [0:5]
|    |   |   |   |   |   microsecond digits:[0:999999]
|    |   |   |   |   |   |
U CA B C B D C B A F C E BCDAAB  
  |    |   |   |   |   | 
  |    |   |   |   |   second: [0:9]
  |    |   |   |   minute: [0:9]
  |    |   |   hour: [0:9]
  |    |   day: [0:9]
  |    month in quarter: [0,1,2]
  year: [0:99]

```