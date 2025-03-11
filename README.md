# Badger 2040 & Badger 2040 W <!-- omit in toc -->

[![MicroPython Firmware](https://github.com/pimoroni/badger2040/actions/workflows/micropython.yml/badge.svg?branch=main)](https://github.com/pimoroni/badger2040/actions/workflows/micropython.yml)
[![Python Linting](https://github.com/pimoroni/badger2040/actions/workflows/python-linting.yml/badge.svg?branch=main)](https://github.com/pimoroni/badger2040/actions/workflows/python-linting.yml)

## RP2040 and Pico W powered E Ink badge wearables<!-- omit in toc -->

This repository contains firmware, examples and documentation for Badger 2040 and Badger 2040 W.

- [Get Badger 2040](#get-badger-2040)
- [Download Firmware](#download-firmware)
- [Installation](#installation)
  - [Badger 2040](#badger-2040)
  - [Badger 2040 W](#badger-2040-w)
- [Useful Links](#useful-links)
- [Other Resources](#other-resources)
  - [Cases and Enclosures](#cases-and-enclosures)

## Get Badger 2040

* [Badger 2040](https://shop.pimoroni.com/products/badger-2040)
* [Badger 2040 W](https://shop.pimoroni.com/products/badger-2040-w)

## Download Firmware

Grab the latest release from [https://github.com/pimoroni/badger2040/releases/latest](https://github.com/pimoroni/badger2040/releases/latest)

There are four .uf2 files to pick from.

:warning: Those marked `with-badger-os` contain a full filesystem image that will overwrite both the firmware *and* filesystem of your Badger:

* pimoroni-badger2040-vX.X.X-micropython-with-badger-os.uf2 
* pimoroni-badger2040w-vX.X.X-micropython-with-badger-os.uf2 

The regular builds just include the firmware, and leave your files alone:

* pimoroni-badger2040-vX.X.X-micropython.uf2 
* pimoroni-badger2040w-vX.X.X-micropython.uf2

## Installation

###  Badger 2040

1. Connect your Badger 2040 to your computer using a USB A to C cable.

2. Reset your device into bootloader mode by holding BOOT/USR and pressing the RST button next to it.

3. Drag and drop one of the `badger2040` .uf2 files to the "RPI-RP2" drive that appears.

4. Your device should reset and, if you used a `with-badger-os` variant, show the Badger OS Launcher.

### Badger 2040 W

1. Connect your Badger 2040 W to your computer using a USB A to microB cable.

2. Reset your device into bootloader mode by holding BOOTSEL (onboard the Pico W) and pressing RESET (next to the qw/st connector). 

3. Drag and drop one of the `badger2040w` .uf2 files to the "RPI-RP2" drive that appears.

4. Your device should reset and, if you used a `with-badger-os` variant, show the Badger OS Launcher.

## Useful Links

* [Function Reference](docs/reference.md)
* [Porting Guide](docs/porting-guide.md)
* [Learn: Getting Started with Badger 2040](https://learn.pimoroni.com/article/getting-started-with-badger-2040)

## Other Resources

Links to community projects and other resources that you might find helpful can be found below. Note that these code examples have not been written/tested by us and we're not able to offer support with them.

* [Send messages to Badger via webform](https://github.com/techcree/Badger2040W/tree/main/webform)
* [Badger Pixel Client for a Raspberry Pi Pixel Server](https://github.com/penguintutor/badger-pixel-client)
* [Badger2040 System II](https://github.com/oneearedrabbit/badger-system-ii)
* [Using Badger 2040 W with Home Assistant and ESPHome](https://community.home-assistant.io/t/anyone-successfully-used-pimoroni-badger-with-esphome/741067/10?u=hellweaver666)

### Cases and Enclosures

* [3D printed Badger 2040 W enclosure](https://kaenner.de/badger2040w)
* [Badger related items on Printables](https://www.printables.com/search/models?q=pimoroni+badger)
