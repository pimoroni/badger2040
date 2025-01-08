#include "hardware/gpio.h"
#include "common/pimoroni_common.hpp"

extern "C" {
#include "system_speed.h"
#include "pico/stdlib.h"
#include "hardware/vreg.h"
#include "hardware/clocks.h"
#include "hardware/pll.h"

#if defined CYW43_WL_GPIO_VBUS_PIN
#include "extmod/modnetwork.h"
#include "lib/cyw43-driver/src/cyw43.h"
#endif

#if MICROPY_HW_ENABLE_UART_REPL
#include "uart.h"
#endif

static void _set_system_speed(uint32_t selected_speed) {
    uint32_t sys_freq;

    switch (selected_speed)
    {
    case 4: // TURBO: 250 MHZ, 1.2V
        vreg_set_voltage(VREG_VOLTAGE_1_20);
        set_sys_clock_khz(250000, true);
        return;
    case 3: // FAST: 133 MHZ
        vreg_set_voltage(VREG_VOLTAGE_1_10);
        set_sys_clock_khz(133000, true);
        return;

    default:
    case 2: // NORMAL: 48 MHZ
        vreg_set_voltage(VREG_VOLTAGE_1_10);
        set_sys_clock_48mhz();
        return;

    case 1: // SLOW: 12 MHZ, 1.0V
        sys_freq = 12 * MHZ;
        break;

    case 0: // VERY_SLOW: 4 MHZ, 1.0V
        sys_freq = 4 * MHZ;
        break;
    }

    // Set the configured clock speed, by dividing the USB PLL
    clock_configure(clk_sys,
                    CLOCKS_CLK_SYS_CTRL_SRC_VALUE_CLKSRC_CLK_SYS_AUX,
                    CLOCKS_CLK_SYS_CTRL_AUXSRC_VALUE_CLKSRC_PLL_USB,
                    48 * MHZ,
                    sys_freq);

    clock_configure(clk_peri,
                    0,
                    CLOCKS_CLK_PERI_CTRL_AUXSRC_VALUE_CLK_SYS,
                    sys_freq,
                    sys_freq);

    clock_configure(clk_adc,
                    0,
                    CLOCKS_CLK_ADC_CTRL_AUXSRC_VALUE_CLKSRC_PLL_USB,
                    48 * MHZ,
                    sys_freq);

    // No longer using the SYS PLL so disable it
    pll_deinit(pll_sys);

    // Not using USB so stop the clock
    clock_stop(clk_usb);

    // Drop the core voltage
    vreg_set_voltage(VREG_VOLTAGE_1_00);
}

static bool _vbus_get() {
    bool vbus = false;
#if defined CYW43_WL_GPIO_VBUS_PIN
    cyw43_gpio_get(&cyw43_state, CYW43_WL_GPIO_VBUS_PIN, &vbus);
#else
    gpio_set_function(PICO_VBUS_PIN, GPIO_FUNC_SIO);
    vbus = gpio_get(PICO_VBUS_PIN);
#endif
    return vbus;
}

mp_obj_t system_speed_vbus_get() {
    return _vbus_get() ? mp_const_true : mp_const_false;
}

mp_obj_t system_speed_set(mp_obj_t speed) {
    uint32_t selected_speed = mp_obj_get_int(speed);

    if (_vbus_get() && selected_speed < 2) {
        // If on USB never go slower than normal speed.
        selected_speed = 2;
    }

    _set_system_speed(selected_speed);

#if MICROPY_HW_ENABLE_UART_REPL
    setup_default_uart();
    mp_uart_init();
#endif

    // TODO Make this work...
    if (selected_speed >= 2) {
        spi_set_baudrate(PIMORONI_SPI_DEFAULT_INSTANCE, 12 * MHZ);
    }
    else {
        // Set the SPI baud rate for communicating with the display to
        // go as fast as possible (which is now 6 or 2 MHz)
        spi_get_hw(PIMORONI_SPI_DEFAULT_INSTANCE)->cpsr = 2;
        hw_write_masked(&spi_get_hw(PIMORONI_SPI_DEFAULT_INSTANCE)->cr0, 0, SPI_SSPCR0_SCR_BITS);
    }

    return mp_const_none;
}

}