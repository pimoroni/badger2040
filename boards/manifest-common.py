include("$(PORT_DIR)/boards/manifest.py")

# HACK: Roundabout way to copy pimoroni.py without modules_py.cmake
freeze("$(PORT_DIR)/../../../pimoroni-pico/micropython/modules_py/", "pimoroni.py")

# Add version.py built by ci/micropython.sh:ci_genversion
freeze("$(PORT_DIR)/../../../", "version.py")

# Handy for dealing with APIs
require("datetime")

