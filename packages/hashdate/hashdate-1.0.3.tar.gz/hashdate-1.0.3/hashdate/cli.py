import time
import sys
import argparse
from hashdate import datetime_to_hash, hash_to_datetime
from colorama import Fore
import datetime
from dateutil.parser import parse

colors = {
    "green": Fore.GREEN,
    "blue": Fore.BLUE,
    "magenta": Fore.MAGENTA,
    "yellow": Fore.YELLOW,
    "red": Fore.RED,
    "reset": Fore.RESET,
}
BASE64_LOGO = """\n\n\n
{yellow}      :::::::::      :::      ::::::::  :::::::::: ::::::::      ::: 
{yellow}     :+:    :+:   :+: :+:   :+:    :+: :+:       :+:    :+:    :+:   
{green}    +:+    +:+  +:+   +:+  +:+        +:+       +:+          +:+ +:+ 
{green}   +#++:++#+  +#++:++#++: +#++:++#++ +#++:++#  +#++:++#+   +#+  +:+  
{green}  +#+    +#+ +#+     +#+        +#+ +#+       +#+    +#+ +#+#+#+#+#+ 
{blue} #+#    #+# #+#     #+# #+#    #+# #+#       #+#    #+#       #+#    
{blue}#########  ###     ###  ########  ########## ########        ### 
{reset}
""".format(
    **colors
)
EMOJI_LOGO = """\n\n\n
{green}███████╗{magenta}███╗   ███╗{green} ██████╗ {magenta}     ██╗{green}██╗
{magenta}██╔════╝{green}████╗ ████║{magenta}██╔═══██╗{green}     ██║{magenta}██║
{green}█████╗  {magenta}██╔████╔██║{green}██║   ██║{magenta}     ██║{green}██║
{magenta}██╔══╝  {green}██║╚██╔╝██║{magenta}██║   ██║{green}██   ██║{magenta}██║
{green}███████╗{magenta}██║ ╚═╝ ██║{green}╚██████╔╝{magenta}╚█████╔╝{green}██║
{magenta}╚══════╝{green}╚═╝     ╚═╝{magenta} ╚═════╝ {green} ╚════╝ {magenta}╚═╝
{reset}
""".format(
    **colors
)
HASHDATE_LOGO = """
{red}                           .x+=:.               
{red}  .uef^"                  z`    ^%    .uef^"    
{red}:d88E                        .   <k :d88E       
{red}`888E             u        .@8Ned8" `888E       
{red} 888E .z8k     us888u.   .@^%8888"   888E .z8k  
{red} 888E~?888L .@88 "8888" x88:  `)8b.  888E~?888L 
{red} 888E  888E 9888  9888  8888N=*8888  888E  888E 
{red} 888E  888E 9888  9888   %8"    R88  888E  888E 
{red} 888E  888E 9888  9888    @8Wou 9%   888E  888E 
{red} 888E  888E 9888  9888  .888888P`    888E  888E 
{red}m888N= 888> "888*""888" `   ^"F     m888N= 888> 
{red} `Y"   888   ^Y"{green}███{red}^Y'{green}╗  █████╗ █████{red}`Y"{green}╗██{red}888{green}██╗
{red}      J88"      {green}██╔══██╗██╔══██╗╚══██╔══╝█{red}J88"{green}══╝
{red}      @%        {green}██║  ██║███████║   ██║   █{red}@%{green}██╗  
{red}    :"          {green}██║  ██║██╔══██║   ██║  {red}:"{green}█╔══╝  
                {green}██████╔╝██║  ██║   ██║   ███████╗
                {green}╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝

{yellow}Hash{green} dates and {yellow}shorten{green} them to the centennial!
{reset}
""".format(
    **colors
)


def show_demo():
    page = "\n" * 80
    print(page)
    for line in HASHDATE_LOGO.split("\n"):
        print(line)
        time.sleep(0.05)

    for c in "{green}...".format(**colors):
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.5)

    print(page)
    text = [
        "{yellow}you can use {green}hashdate{yellow} to create hashes from datetimes\n"
        "{yellow}for example:\n"
        "  the date {green}2020-05-13T22:30:47.136450\n"
        "  {yellow}becomes {green}UCABCBDCCDAEHBDGEFA\n"
        "\n{yellow}... If you are using {green}base64 charset {yellow}that is.\n",
        "\n{yellow}hashes produced by {green}hashdate {yellow}are shortable prefixes.\n"
        "{yellow}that means you can shorten them\n"
        "                             from {green}right\n"
        "{yellow}to {green}left\n"
        "\n{yellow}and loose precision.\n",
        "\n{yellow}lets take the previous example again:\n",
        "\n{green}2020-05-13T22:30:47.136450",
        "\n\n{yellow}was turned into the following hash:",
        "\n\n{green}UCABCBDCCDAEHBDGEFA\n",
        "\n{yellow}now if we wanna {green}reduce {yellow}precision to the {green}minute\n"
        "{yellow}we would only take the {green}first 11 chars {yellow} of the hash:\n"
        "\n{green}UCABCBDCCDA{yellow}EHBDGEFA\n"
        "\nwhen we run that hash {green}UCABCBDCCDA {yellow}through the {green}hash_to_datetime\n"
        "{yellow}we get:\n"
        "\n{green}2020-05-13T22:30:00\n",
        "\n{yellow}here you can see we have reduced precision to {green}the minute",
        "\n\n{green}hashdate's {yellow}are structured like this:\n",
    ]
    diagram = [
        "\n\n{green}centenial{yellow}: [...19,20,21...]",
        "{yellow}|    {green}quarter start month{yellow}: [0,3,6,9]",
        "{yellow}|    |   {green}day in tens{yellow}: [0:3]",
        "{yellow}|    |   |   {green}hour in tens{yellow}: [0:5]",
        "{yellow}|    |   |   |   {green}minute in tens{yellow}: [0:5]",
        "{yellow}|    |   |   |   |   {green}second in tens{yellow}: [0:5]",
        "{yellow}|    |   |   |   |   |   {green}microsecond digits{yellow}:[0:999999]",
        "{yellow}|    |   |   |   |   |   |",
        "{green}U CA B C B D C B A F C E BCDAAB  ",
        "{yellow}  |    |   |   |   |   | ",
        "{yellow}  |    |   |   |   |   {green}second{yellow}: [0:9]",
        "{yellow}  |    |   |   |   {green}minute{yellow}: [0:9]",
        "{yellow}  |    |   |   {green}hour{yellow}: [0:9]",
        "{yellow}  |    |   {green}day{yellow}: [0:9]",
        "{yellow}  |    {green}month in quarter{yellow}: [0,1,2]",
        "  {green}year{yellow}: [0:99]",
    ]
    for line in text:
        line = line.format(**colors)

        for c in line:
            sys.stdout.write(c)
            sys.stdout.flush()
            time.sleep(0.05)
        time.sleep(1.5)

    for line in diagram:
        print(line.format(**colors))
        time.sleep(0.05)

    time.sleep(3)

    text = [
        "\n\n{green}hashdate {yellow}also supports using {green}emojis {yellow}as charset",
        "\n{yellow}we will now see how it all looks" "\n\nits {green}demo time!!!",
    ]
    for line in text:
        line = line.format(**colors)
        for c in line:
            sys.stdout.write(c)
            sys.stdout.flush()
            time.sleep(0.05)

    time.sleep(2)

    def inner_demo(charset):
        header = "{yellow}{date}{green}{hash}".format(
            date="datetime".ljust(30), hash="hash", **colors
        )
        print(header)
        print(("{magenta}" + "_" * len(header)).format(**colors))
        print()
        time.sleep(2)
        for i in range(10):
            now = datetime.datetime.now()
            hash = datetime_to_hash(now, charset)
            print(
                "{yellow}{date}{green}{hash}".format(
                    date=now.isoformat().ljust(30), hash=hash, **colors
                )
            )
            time.sleep(0.05)

        sign = -1
        sub = 0
        for i in range(17 * 3):
            time.sleep(0.05)
            now = datetime.datetime.now()
            hash = datetime_to_hash(now, charset)
            if i % 17 == 0:
                sign *= -1
            subhash = hash[: len(hash) - (sub)]
            dt = hash_to_datetime(subhash, charset)
            print(
                "{magenta}{date}{green}{hash}".format(
                    date=dt.isoformat().ljust(30), hash=subhash, **colors
                )
            )
            sub += sign

    for line in BASE64_LOGO.split("\n"):
        print(line)
        time.sleep(0.05)

    inner_demo("base64")

    for line in EMOJI_LOGO.split("\n"):
        print(line)
        time.sleep(0.05)

    inner_demo("emoji")

    text = [
        "\n\n{green}hashdate {yellow}is fun to use and fun to look at!",
        "\n{yellow}see you at {green}https://github.com/sloev/hashdate"
        "\n\n{magenta} - sloev",
    ]
    for line in text:
        line = line.format(**colors)
        for c in line:
            sys.stdout.write(c)
            sys.stdout.flush()
            time.sleep(0.05)
    print("\n" * 2)
    for line in HASHDATE_LOGO.split("\n"):
        print(line)
        time.sleep(0.05)


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", "-v", action="store_true")

    commands = parser.add_subparsers(title="commands", dest="command")

    commands.add_parser("demo")
    # fancy_filters_parser.add_argument("-n", type=int, default=5000)
    # fancy_filters_parser.add_argument("-o", type=argparse.FileType("w"), default="jobs.json")
    # fancy_filters_parser.add_argument("-a", type=argparse.FileType("r"), default="aspects.txt")

    date2hash_parser = commands.add_parser("date2hash")
    date2hash_parser.add_argument("datetime", type=parse)
    date2hash_parser.add_argument(
        "--charset", "-c", type=str, default="base64", help="charset [base64, emoji]"
    )

    hash2date_parser = commands.add_parser("hash2date")
    hash2date_parser.add_argument("hash", type=str)
    hash2date_parser.add_argument(
        "--charset", "-c", type=str, default="base64", help="charset [base64, emoji]"
    )

    options, argv = parser.parse_known_args(sys.argv[1:])

    try:
        if options.command == "demo":
            show_demo()
        elif options.command == "date2hash":
            hash = datetime_to_hash(options.datetime, options.charset)
            print("{yellow}hash: {green}{hash}".format(hash=hash, **colors))
        elif options.command == "hash2date":
            dt = hash_to_datetime(options.hash, options.charset)
            print(
                "{yellow}datetime: {green}{datetime}".format(
                    datetime=dt.isoformat(), **colors
                )
            )
    except:
        if options.verbose:
            raise
        else:
            print("{red}Error, exciting (run with -v for more info)".format(**colors))
