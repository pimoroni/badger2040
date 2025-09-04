if(NOT DEFINED PIMORONI_PICO_PATH)
set(PIMORONI_PICO_PATH ${CMAKE_CURRENT_LIST_DIR}/../pimoroni-pico)
endif()
include(${PIMORONI_PICO_PATH}/pimoroni_pico_import.cmake)

include_directories(${CMAKE_CURRENT_LIST_DIR}/../../)
include_directories(${PIMORONI_PICO_PATH}/micropython)

# Drivers, etc
list(APPEND CMAKE_MODULE_PATH "${PIMORONI_PICO_PATH}")
# modules_py/modules_py
list(APPEND CMAKE_MODULE_PATH "${PIMORONI_PICO_PATH}/micropython")
# All regular modules
list(APPEND CMAKE_MODULE_PATH "${PIMORONI_PICO_PATH}/micropython/modules")

# Allows us to find downstream /cmodules/
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/..")

# Enable support for string_view (for PicoGraphics)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

# Essential
include(pimoroni_i2c/micropython)
include(pimoroni_bus/micropython)

# Pico Graphics Essential
include(hershey_fonts/micropython)
include(bitmap_fonts/micropython)
include(picographics/micropython)

# Pico Graphics Extra
include(jpegdec/micropython)
include(pngdec/micropython)
include(qrcode/micropython/micropython)

# Sensors & Breakouts
include(micropython-common-breakouts)
include(pcf85063a/micropython)

# Utility
include(adcfft/micropython)

# Use our LOCAL wakeup module from firmware/modules/wakeup
include(cmodules/wakeup/micropython)
if(MICROPY_BOARD EQUAL "PICO_W")
target_compile_definitions(usermod_wakeup INTERFACE
    -DWAKEUP_HAS_RTC=1
    -DWAKEUP_PIN_MASK=0b10000000000010000000000
    -DWAKEUP_PIN_DIR=0b10000000000010000000000
    -DWAKEUP_PIN_VALUE=0b10000000000010000000000
)
else()
target_compile_definitions(usermod_wakeup INTERFACE
    -DWAKEUP_PIN_MASK=0b10000000000000010000000000
    -DWAKEUP_PIN_DIR=0b10000000000000010000000000
    -DWAKEUP_PIN_VALUE=0b10000000000000010000000000
)
endif()

# LEDs & Matrices
include(plasma/micropython)

# Servos & Motors
include(pwm/micropython)
include(servo/micropython)
include(encoder/micropython)
include(motor/micropython)

# C++ Magic Memory
include(cppmem/micropython)

# Disable build-busting C++ exceptions
include(micropython-disable-exceptions)