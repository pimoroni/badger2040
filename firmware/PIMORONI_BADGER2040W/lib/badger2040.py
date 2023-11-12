import machine
import micropython
from picographics import PicoGraphics, DISPLAY_INKY_PACK
import time
import wakeup
import pcf85063a
import cppmem


BUTTON_DOWN = 11
BUTTON_A = 12
BUTTON_B = 13
BUTTON_C = 14
BUTTON_UP = 15
BUTTON_USER = None  # User button not available on W

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

RTC_ALARM = 8
LED = 22
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
}

WAKEUP_MASK = 0

i2c = machine.I2C(0)
rtc = pcf85063a.PCF85063A(i2c)
i2c.writeto_mem(0x51, 0x00, b'\x00')  # ensure rtc is running (this should be default?)
rtc.enable_timer_interrupt(False)

enable = machine.Pin(ENABLE_3V3, machine.Pin.OUT)
enable.on()

cppmem.set_mode(cppmem.MICROPYTHON)


def is_wireless():
    return True


def woken_by_rtc():
    return bool(wakeup.get_gpio_state() & (1 << RTC_ALARM))


def woken_by_button():
    return wakeup.get_gpio_state() & BUTTON_MASK > 0


def pressed_to_wake(button):
    return wakeup.get_gpio_state() & (1 << button) > 0


def reset_pressed_to_wake():
    wakeup.reset_gpio_state()


def pressed_to_wake_get_once(button):
    global WAKEUP_MASK
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
    # until an RTC alarm or button event
    rtc_alarm = machine.Pin(RTC_ALARM)
    while True:
        if rtc_alarm.value():
            return
        for button in BUTTONS.values():
            if button.value():
                return


def pico_rtc_to_pcf():
    # Set the PCF85063A to the time stored by Pico W's RTC
    year, month, day, dow, hour, minute, second, _ = machine.RTC().datetime()
    rtc.datetime((year, month, day, hour, minute, second, dow))


def pcf_to_pico_rtc():
    # Set Pico W's RTC to the time stored by the PCF85063A
    t = rtc.datetime()
    # BUG ERRNO 22, EINVAL, when date read from RTC is invalid for the Pico's RTC.
    try:
        machine.RTC().datetime((t[0], t[1], t[2], t[6], t[3], t[4], t[5], 0))
        return True
    except OSError:
        return False


def sleep_for(minutes):
    year, month, day, hour, minute, second, dow = rtc.datetime()

    # if the time is very close to the end of the minute, advance to the next minute
    # this aims to fix the edge case where the board goes to sleep right as the RTC triggers, thus never waking up
    if second >= 55:
        minute += 1

    # Can't sleep beyond a month, so clamp the sleep to a 28 day maximum
    minutes = min(minutes, 40320)

    # Calculate the future alarm date; first, turn the current time into seconds since epoch
    sec_since_epoch = time.mktime((year, month, day, hour, minute, second, dow, 0))

    # Add the required minutes to this
    sec_since_epoch += minutes * 60

    # And convert it back into a more useful tuple
    (ayear, amonth, aday, ahour, aminute, asecond, adow, adoy) = time.localtime(sec_since_epoch)

    # And now set the alarm as before, now including the day
    rtc.clear_alarm_flag()
    rtc.set_alarm(0, aminute, ahour, aday)
    rtc.enable_alarm_interrupt(True)

    turn_off()


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
        return BUTTONS[button].value() == 1 or pressed_to_wake_get_once(button)

    def pressed_any(self):
        for button in BUTTONS.values():
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

    def status_handler(self, mode, status, ip):
        self.display.set_update_speed(2)
        print(mode, status, ip)
        self.display.set_pen(15)
        self.display.clear()
        self.display.set_pen(0)
        if status:
            self.display.text("Connected!", 10, 10, 300, 0.5)
            self.display.text(ip, 10, 30, 300, 0.5)
        else:
            self.display.text("Connecting...", 10, 10, 300, 0.5)
        self.update()

    def isconnected(self):
        import network
        return network.WLAN(network.STA_IF).isconnected()

    def ip_address(self):
        import network
        return network.WLAN(network.STA_IF).ifconfig()[0]

    def connect(self, **args):
        from network_manager import NetworkManager
        import WIFI_CONFIG
        import uasyncio
        import gc

        status_handler = args.get("status_handler", self.status_handler)

        if WIFI_CONFIG.COUNTRY == "":
            raise RuntimeError("You must populate WIFI_CONFIG.py for networking.")

        network_manager = NetworkManager(WIFI_CONFIG.COUNTRY, status_handler=status_handler)
        uasyncio.get_event_loop().run_until_complete(network_manager.client(WIFI_CONFIG.SSID, WIFI_CONFIG.PSK))
        gc.collect()
