# xkcd

[![Join the chat at https://gitter.im/xkcd-script/xkcd](https://badges.gitter.im/xkcd-script/xkcd.svg)](https://gitter.im/xkcd-script/xkcd?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)![GitHub repo size](https://img.shields.io/github/repo-size/brayo-pip/xkcd)![License](https://img.shields.io/github/license/brayo-pip/xkcd)

This is a script for downloading all the xkcd comics

## How to use the script

clone the repo

```console
$git clone https://xkcd.com/brayo-pip/xkcd.git
```

Run this code to install all the dependencies

```console
$cd xkcd
```

```console
$pip3 install -r requirements.txt
```

Then run the script.

```console
$python xkcd/download.py
```

## How this script is better than most of the other scripts

I can't say for sure that this is the best script for downloading xkcd comics there is,
but I can say it's one of the fastest. The script uses persistent http connections which I haven't yet seen in another xkcd script.
The script skips previously downloaded comics and skips non-image comics such as js-scripts, it however highlights you of this and provides you with a link should you wish to visit the site yourself and see the 'interactive comic'.

## Other technical features

The script maintains a continuity file so that it can 'recall' the last comic it downloaded.
It does updates the continuity file every 10 comics, I didn't want to update too often as this could be a bottleneck.
The continuity file is also updated during this 'sleep' session.

The script also has an amateur network congestion control, simply sleeps for 0.5 seconds for every 10 comics downloaded.This may be necessary once I introduce multi-threading.

## Upcoming features

Finally introduced concurrency it's available on concurrent branch. I am still debuging it, but it works perfectly 99% of the time,xd.
