include("$(PORT_DIR)/boards/manifest.py")

freeze("lib/")

# mip, ntptime, urequests, webrepl etc - see:
# https://github.com/micropython/micropython-lib/blob/master/micropython/bundles/bundle-networking/manifest.py
require("bundle-networking")

# Bluetooth
require("aioble")

require("urllib.urequest")
require("umqtt.simple")