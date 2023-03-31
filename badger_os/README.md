# Badger 2040 MicroPython Examples <!-- omit in toc -->

These MicroPython examples demonstrate a variety of applications and are distributed as a sort of "OS" for Badger 2040.

They should help you get started quickly and give you something to modify for your own requirements.

- [Examples](#examples)
  - [Badge](#badge)
  - [Clock](#clock)
  - [Ebook](#ebook)
  - [Fonts](#fonts)
  - [Help](#help)
  - [Image](#image)
  - [Info](#info)
  - [List](#list)
  - [Net Info](#net-info)
  - [News](#news)
  - [Qrgen](#qrgen)
  - [Weather](#weather)
- [Other Resources](#other-resources)

## Examples

Find out more about how to use these examples in our Learn guide:

- [Getting Started with Badger 2040 W](https://learn.pimoroni.com/article/getting-started-with-badger-2040-w)

### Badge
[badge.py](examples/badge.py)

Customisable name badge example.

Loads badge details from the `/badges` directory on the device, using a file called `badge.txt` which should contain:

* Company
* Name
* Detail 1 title
* Detail 1 text
* Detail 2 title
* Detail 2 text
* Badge image path

For example:

```txt
mustelid inc
H. Badger
RP2040
2MB Flash
E ink
296x128px
/badges/badge.jpg
```

The image should be a 104x128 pixel JPEG. Any colours other than black/white will be dithered.

### Clock
[clock.py](examples/clock.py)

Clock example with (optional) NTP synchronization and partial screen updates. 

Press button B to switch the clock into time set mode.

On Badger 2040 this allows you to set the internal RTC, but it will not survive a sleep/wake cycle even with a connected battery.

On Badger 2040 W it will set the external RTC and the time will persist even after sleep/wake.

### Ebook
[ebook.py](examples/ebook.py)

View text files on Badger.

Currently reads an abridged copy of "The Wind in the Willows" out of the `/books` directory.

### Fonts
[fonts.py](examples/fonts.py)

A basic example that lets you preview how all of the built-in fonts will appear on the display.

### Help
[help.py](examples/help.py)

Gives instructions on to navigate the launcher.

### Image
[image.py](examples/image.py)

Display JPEG images. Images are read out of the `/images` directory on device.

Press button B to show/hide the image filename.

### Info
[info.py](examples/info.py)

Info about Badger 2040.

### List
[list.py](examples/list.py)

A checklist to keep track of to-dos or shopping. Use A/C and Up/Down to navigate and B to check/uncheck items.

### Net Info
[net_info.py](examples/net_info.py)

Show IP address and other wireless connection details.

### News
[news.py](examples/news.py)

View BBC news headlines.

### Qrgen
[qrgen.py](examples/qrgen.py)

Display QR codes and associated text.

### Weather
[weather.py](examples/weather.py)

Display current weather data from the [Open-Meteo weather API](https://open-meteo.com/)

## Other Resources

Here are some cool Badger-related community projects and resources that you might find useful / inspirational! Note that code at the links below has not been tested by us and we're not able to offer support with it.

- :link: [Send messages to Badger via webform](https://github.com/techcree/Badger2040W/tree/main/webform)
- :link: [3D printed Badger 2040 W enclosure](https://kaenner.de/badger2040w)
- :link: [Badger Pixel Client for a Raspberry Pi Pixel Server](https://github.com/penguintutor/badger-pixel-client)
- :link: [Badger2040 System II](https://github.com/oneearedrabbit/badger-system-ii)
