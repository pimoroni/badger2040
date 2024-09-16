# cmake file for Pimoroni Badger 2350
set(PICO_BOARD "pimoroni_badger2350")
set(PICO_PLATFORM "rp2350")

# Make sure we find pimoroni_badger2350.h (PICO_BOARD) in the current dir
set(PICO_BOARD_HEADER_DIRS ${CMAKE_CURRENT_LIST_DIR})

# Board specific version of the frozen manifest
set(MICROPY_FROZEN_MANIFEST ${CMAKE_CURRENT_LIST_DIR}/manifest.py)

set(MICROPY_C_HEAP_SIZE 4096)