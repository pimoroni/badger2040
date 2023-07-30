# Badger 2040 & Badger 2040 W <!-- omit in toc -->
## Firmware, Examples & Documentation <!-- omit in toc -->

Badger 2040 and Badger 2040 W are maker-friendly all-in-one badge wearables, featuring a 2.9", 296x128 pixel, monochrome e-paper display.

- [Install](#install)
  - [Badger 2040](#badger-2040)
  - [Badger 2040 W](#badger-2040-w)

## Install

Grab the latest release from [https://github.com/pimoroni/badger2040/releases/latest](https://github.com/pimoroni/badger2040/releases/latest)

There are four .uf2 files to pick from.

:warning: Those marked `with-badger-os` contain a full filesystem image that will overwrite both the firmware *and* filesystem of your Badger:

* pimoroni-badger2040-vX.X.X-micropython-with-badger-os.uf2 
* pimoroni-badger2040w-vX.X.X-micropython-with-badger-os.uf2 

The regular builds just include the firmware, and leave your files alone:

* pimoroni-badger2040-vX.X.X-micropython.uf2 
* pimoroni-badger2040w-vX.X.X-micropython.uf2

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
