import machine
import micropython
from picographics import PicoGraphics, DISPLAY_INKY_PACK
import time
import wakeup
import cppmem


BUTTON_DOWN = 11
BUTTON_A = 12
BUTTON_B = 13
BUTTON_C = 14
BUTTON_UP = 15
BUTTON_USER = 23

BUTTON_MASK = 0b11111 << 11

SYSTEM_VERY_SLOW = 0
SYSTEM_SLOW = 1
SYSTEM_NORMAL = 2
SYSTEM_FAST = 3
SYSTEM_TURBO = 4

UPDATE_NORMAL = 0
UPDATE_MEDIUM = 1
UPDATE_FAST = 2
UPDATE_TURBO = 3

LED = 25
ENABLE_3V3 = 10
BUSY = 26

WIDTH = 296
HEIGHT = 128

SYSTEM_FREQS = [
    4000000,
    12000000,
    48000000,
    133000000,
    250000000
]

BUTTONS = {
    BUTTON_DOWN: machine.Pin(BUTTON_DOWN, machine.Pin.IN, machine.Pin.PULL_DOWN),
    BUTTON_A: machine.Pin(BUTTON_A, machine.Pin.IN, machine.Pin.PULL_DOWN),
    BUTTON_B: machine.Pin(BUTTON_B, machine.Pin.IN, machine.Pin.PULL_DOWN),
    BUTTON_C: machine.Pin(BUTTON_C, machine.Pin.IN, machine.Pin.PULL_DOWN),
    BUTTON_UP: machine.Pin(BUTTON_UP, machine.Pin.IN, machine.Pin.PULL_DOWN),
    BUTTON_USER: machine.Pin(BUTTON_USER, machine.Pin.IN, machine.Pin.PULL_UP),
}

WAKEUP_MASK = 0

enable = machine.Pin(ENABLE_3V3, machine.Pin.OUT)
enable.on()

cppmem.set_mode(cppmem.MICROPYTHON)


def is_wireless():
    return False


def woken_by_rtc():
    return False  # Badger 2040 does not include an RTC


def woken_by_button():
    return wakeup.get_gpio_state() & BUTTON_MASK > 0


def pressed_to_wake(button):
    return wakeup.get_gpio_state() & (1 << button) > 0


def reset_pressed_to_wake():
    wakeup.reset_gpio_state()


def pressed_to_wake_get_once(button):
    global WAKEUP_MASK
    if button == BUTTON_USER:
        return False
    result = (wakeup.get_gpio_state() & ~WAKEUP_MASK & (1 << button)) > 0
    WAKEUP_MASK |= (1 << button)
    return result


def system_speed(speed):
    try:
        machine.freq(SYSTEM_FREQS[speed])
    except IndexError:
        pass


def turn_on():
    enable.on()


def turn_off():
    time.sleep(0.05)
    enable.off()
    # Simulate an idle state on USB power by blocking
    # until a button event
    while True:
        for pin, button in BUTTONS.items():
            if pin == BUTTON_USER:
                if not button.value():
                    return
                continue
            if button.value():
                return


def sleep_for(minutes=None):
    raise RuntimeError("Badger 2040 does not include an RTC.")


pico_rtc_to_pcf = pcf_to_pico_rtc = sleep_for


class Badger2040():
    def __init__(self):
        self.display = PicoGraphics(DISPLAY_INKY_PACK)
        self._led = machine.PWM(machine.Pin(LED))
        self._led.freq(1000)
        self._led.duty_u16(0)
        self._update_speed = 0

    def __getattr__(self, item):
        # Glue to redirect calls to PicoGraphics
        return getattr(self.display, item)

    def update(self):
        t_start = time.ticks_ms()
        self.display.update()
        t_elapsed = time.ticks_ms() - t_start

        delay_ms = [4700, 2600, 900, 250][self._update_speed]

        if t_elapsed < delay_ms:
            time.sleep((delay_ms - t_elapsed) / 1000)

    def set_update_speed(self, speed):
        self.display.set_update_speed(speed)
        self._update_speed = speed

    def led(self, brightness):
        brightness = max(0, min(255, brightness))
        self._led.duty_u16(int(brightness * 256))

    def invert(self, invert):
        raise RuntimeError("Display invert not supported in PicoGraphics.")

    def thickness(self, thickness):
        raise RuntimeError("Thickness not supported in PicoGraphics.")

    def halt(self):
        turn_off()

    def keepalive(self):
        turn_on()

    def pressed(self, button):
        return BUTTONS[button].value() == (0 if button == BUTTON_USER else 1) or pressed_to_wake_get_once(button)

    def pressed_any(self):
        for pin, button in BUTTONS.items():
            if pin == BUTTON_USER:
                if not button.value():
                    return True
                continue
            if button.value():
                return True
        return False

    @micropython.native
    def icon(self, data, index, data_w, icon_size, x, y):
        s_x = (index * icon_size) % data_w
        s_y = int((index * icon_size) / data_w)

        for o_y in range(icon_size):
            for o_x in range(icon_size):
                o = ((o_y + s_y) * data_w) + (o_x + s_x)
                bm = 0b10000000 >> (o & 0b111)
                if data[o >> 3] & bm:
                    self.display.pixel(x + o_x, y + o_y)

    def image(self, data, w, h, x, y):
        for oy in range(h):
            row = data[oy]
            for ox in range(w):
                if row & 0b1 == 0:
                    self.display.pixel(x + ox, y + oy)
                row >>= 1

    def isconnected(self):
        return False

    def ip_address(self):
        return (0, 0, 0, 0)

    def connect(self):
        pass
