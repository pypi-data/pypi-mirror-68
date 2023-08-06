import datetime

MAX_HASH_LENGTH = 19
BUILTIN_CHARSETS = {}


def register_charset(charset_name, charset):
    BUILTIN_CHARSETS[charset_name] = {"zero": charset[0]}
    for index, c in enumerate(charset):
        BUILTIN_CHARSETS[charset_name][index] = c
        BUILTIN_CHARSETS[charset_name][c] = index


BUILTIN_CHARSETS_RAW = {
    "emoji": "🌼🥕🐲🌲🍇🐂🌴🐐🍉🌺🍊🐽🍆🦎🍟🌱🐫🐍🐃🍍🌹🍕☘🌿🥓🐪🌷🏵🔥🐷🌳🌶🥒🐊🐗🐏🌵🌻🌽🐢🍋🍈💮🎃🌊🥔🌰🍀🍃💧💐🍂🐮🌸🐄🍄🍁🍞🥜🐑🥀🌭🐸🐖",
    "base64": "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",
}

for charset_name, charset in BUILTIN_CHARSETS_RAW.items():
    register_charset(charset_name, charset)


def get_lookup(charset):
    try:
        charset_lookup = BUILTIN_CHARSETS[charset]
    except KeyError:
        raise RuntimeError(
            "charset {} is not supported!, please register it first!".format(charset)
        )
    return charset_lookup


def datetime_to_hash(dt, charset="base64"):
    lookup = get_lookup(charset)
    value = ""
    year = "{:04d}".format(dt.year)
    value += lookup[int(year[:2])]
    value += lookup[int(year[2])]
    value += lookup[int(year[3])]

    quarter = int(dt.month / 3)
    value += lookup[quarter]

    quarter_month = dt.month % 3
    value += lookup[quarter_month]

    value += "".join(
        lookup[int(c)]
        for c in "{:02d}{:02d}{:02d}{:02d}{:06d}".format(
            dt.day, dt.hour, dt.minute, dt.second, dt.microsecond
        )
    )

    return value


def hash_to_datetime(hash, charset="base64"):
    lookup = get_lookup(charset)
    # print(lookup, hash, len(hash))
    padded_hash = [
        lookup[c] for c in list(hash) + (MAX_HASH_LENGTH - len(hash)) * [lookup["zero"]]
    ]
    (
        year_0,
        year_1,
        year_2,
        quarter,
        quarter_month,
        day_0,
        day_1,
        hour_0,
        hour_1,
        minute_0,
        minute_1,
        second_0,
        second_1,
        microsecond_0,
        microsecond_1,
        microsecond_2,
        microsecond_3,
        microsecond_4,
        microsecond_5,
    ) = padded_hash

    year = int("{}{}{}".format(year_0, year_1, year_2))
    month = quarter * 3 + quarter_month
    microsecond = int(
        "{}{}{}{}{}{}".format(
            microsecond_0,
            microsecond_1,
            microsecond_2,
            microsecond_3,
            microsecond_4,
            microsecond_5,
        )
    )

    return datetime.datetime(
        year,
        month or 1,
        int("{}{}".format(day_0, day_1)) or 1,
        int("{}{}".format(hour_0, hour_1)),
        int("{}{}".format(minute_0, minute_1)),
        int("{}{}".format(second_0, second_1)),
        microsecond,
    )
