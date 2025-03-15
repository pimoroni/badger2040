// This is a hack! Need to replace with upstream board definition.
#define MICROPY_HW_BOARD_NAME          "Pimoroni Badger2040W 2MB"
#define MICROPY_HW_FLASH_STORAGE_BYTES          (848 * 1024)

// Enable networking.
#define MICROPY_PY_NETWORK 1
#define MICROPY_PY_NETWORK_HOSTNAME_DEFAULT     "Badger2040W"

// CYW43 driver configuration.
#define CYW43_USE_SPI (1)
#define CYW43_LWIP (1)
#define CYW43_GPIO (1)
#define CYW43_SPI_PIO (1)
#define CYW43_WL_GPIO_VBUS_PIN (2)

// For debugging mbedtls - also set
// Debug level (0-4) 1=warning, 2=info, 3=debug, 4=verbose
// #define MODUSSL_MBEDTLS_DEBUG_LEVEL 1

#define MICROPY_HW_PIN_EXT_COUNT    CYW43_WL_GPIO_COUNT

#define MICROPY_HW_PIN_RESERVED(i) ((i) == CYW43_PIN_WL_HOST_WAKE || (i) == CYW43_PIN_WL_REG_ON)