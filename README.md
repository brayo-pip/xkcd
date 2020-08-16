# xkcd
This is a script for downloading all the xkcd comics

## How to use the script
clone the repo
```console 
$git clone https://xkcd.com/brayo-pip/xkcd.git
```
Then run the script.
```console
$python xkcd/download.py
```
## How this script is better than most of the other scripts
I can't say for sure that this is the best script for downloading xkcd comics there is,
but I can say it's one of the fastest. The script uses persistent http connections which I haven't yet seen in another xkcd script.
The script skips previously downloaded comics and skips non-image comics such as js-scripts, it however highlights you of this and provides you with a link should you wish to visit the site yourself and see the 'interactive comic'

## Other technical features
The script maintains a continuity file so that it can 'recall' the last comic it downloaded.
It does updates the continuity file every 50 comics, I didn't want to update too often as this could be a bottleneck.
The continuity file is also updated during this 'sleep' session.

The script also has an amateur network congestion control, simply sleeps for 0.5 seconds for every 10 comics downloaded.This may be necessary once I introduce multithreading.

## Upcoming features
I wish to introduce multithreading so as to be able to fully utilize the a user's bandwidth. Requesting multiple comics simultaneously and writing them to disk/SSD simultaneously.