pdftoogg
========

A short Python script that converts a pdf into an ogg file. Created this so that I could listen PDF documents for my studies while on the train to work. I've only tested it on debian, but it should work on any Linux system. It produces a few error that I need to look into and I could neaten up a few of the for loops and whatnot to make it a bit nice to read.
To install rename the file to remove the extention.
```mv pdftoogg.py pdftoogg``` and install it into /urs/bin 
```sudo install -m 755 pdftoogg /usr/bin```


Ideas and bits of code shamelessly ripped from http://picospeaker.tk/ and https://github.com/redacted/XKCD-password-generator

Requires pdftotext (Should be on most linux systems) and pico2wave which can be found by ```sudo apt-get install libttspico0 libttspico-data libttspico-utils```

This is free and unencumbered software released into the public domain.
