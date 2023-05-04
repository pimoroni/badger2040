# cmake file for Pimoroni Badger 2040
set(MICROPY_BOARD PICO)

# Board specific version of the frozen manifest
set(MICROPY_FROZEN_MANIFEST ${CMAKE_CURRENT_LIST_DIR}/manifest.py)

set(MICROPY_C_HEAP_SIZE 4096)