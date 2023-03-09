include("$(PORT_DIR)/boards/manifest.py")

freeze("lib/")

require("mip")
require("ntptime")
require("urequests")
require("urllib.urequest")
require("umqtt.simple")