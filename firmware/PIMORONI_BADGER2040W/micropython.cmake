set(PIMORONI_PICO_PATH ../../../../pimoroni-pico)
include(${CMAKE_CURRENT_LIST_DIR}/../pimoroni_pico_import.cmake)

include_directories(${PIMORONI_PICO_PATH}/micropython)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/../../")
list(APPEND CMAKE_MODULE_PATH "${PIMORONI_PICO_PATH}/micropython")
list(APPEND CMAKE_MODULE_PATH "${PIMORONI_PICO_PATH}/micropython/modules")

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
include(firmware/modules/wakeup/micropython)
target_compile_definitions(usermod_wakeup INTERFACE
    -DWAKEUP_HAS_RTC=1
    -DWAKEUP_PIN_MASK=0b10000000000010000000000
    -DWAKEUP_PIN_DIR=0b10000000000010000000000
    -DWAKEUP_PIN_VALUE=0b10000000000010000000000
)

# Note: cppmem is *required* for C++ code to function on MicroPython
# it redirects `malloc` and `free` calls to MicroPython's heap
include(cppmem/micropython)

# LEDs & Matrices
include(plasma/micropython)

# Servos & Motors
include(pwm/micropython)
include(servo/micropython)
include(encoder/micropython)
include(motor/micropython)

# version.py, pimoroni.py and boot.py
include(modules_py/modules_py)

# TODO: Use `include(micropython-disable-exceptions)`
# Do not include stack unwinding & exception handling for C++ user modules
target_compile_definitions(usermod INTERFACE PICO_CXX_ENABLE_EXCEPTIONS=0)
target_compile_options(usermod INTERFACE $<$<COMPILE_LANGUAGE:CXX>:
    -fno-exceptions
    -fno-unwind-tables
    -fno-rtti
    -fno-use-cxa-atexit
>)
target_link_options(usermod INTERFACE -specs=nano.specs)
