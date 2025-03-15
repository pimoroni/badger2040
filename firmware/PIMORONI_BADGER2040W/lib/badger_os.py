import os
import gc
import time
import json
import machine
import badger2040


def get_battery_level():
    from machine import Pin, ADC

    # Setup pins
    Pin(25, Pin.OUT, value=1)  # Deselect Wi-Fi module
    Pin(29, Pin.IN, pull=None)  # Set VSYS ADC pin floating

    # VSYS measurement
    vsys_adc = ADC(29)
    vsys = (vsys_adc.read_u16() / 65535) * 3 * 3.3

    return vsys


def get_disk_usage():
    # f_bfree and f_bavail should be the same?
    # f_files, f_ffree, f_favail and f_flag are unsupported.
    f_bsize, f_frsize, f_blocks, f_bfree, _, _, _, _, _, f_namemax = os.statvfs("/")

    f_total_size = f_frsize * f_blocks
    f_total_free = f_bsize * f_bfree
    f_total_used = f_total_size - f_total_free

    f_used = 100 / f_total_size * f_total_used
    f_free = 100 / f_total_size * f_total_free

    return f_total_size, f_used, f_free


def state_running():
    state = {"running": "launcher"}
    state_load("launcher", state)
    return state["running"]


def state_clear_running():
    running = state_running()
    state_modify("launcher", {"running": "launcher"})
    return running != "launcher"


def state_set_running(app):
    state_modify("launcher", {"running": app})


def state_launch():
    app = state_running()
    if app is not None and app != "launcher":
        launch(app)


def state_delete(app):
    try:
        os.remove("/state/{}.json".format(app))
    except OSError:
        pass


def state_save(app, data):
    try:
        with open("/state/{}.json".format(app), "w") as f:
            f.write(json.dumps(data))
            f.flush()
    except OSError:
        import os
        try:
            os.stat("/state")
        except OSError:
            os.mkdir("/state")
            state_save(app, data)


def state_modify(app, data):
    state = {}
    state_load(app, state)
    state.update(data)
    state_save(app, state)


def state_load(app, defaults):
    try:
        data = json.loads(open("/state/{}.json".format(app), "r").read())
        if type(data) is dict:
            defaults.update(data)
            return True
    except (OSError, ValueError):
        pass

    state_save(app, defaults)
    return False


def launch(file):
    state_set_running(file)

    gc.collect()

    button_a = machine.Pin(badger2040.BUTTON_A, machine.Pin.IN, machine.Pin.PULL_DOWN)
    button_c = machine.Pin(badger2040.BUTTON_C, machine.Pin.IN, machine.Pin.PULL_DOWN)

    def quit_to_launcher(pin):
        if button_a.value() and button_c.value():
            machine.reset()

    button_a.irq(trigger=machine.Pin.IRQ_RISING, handler=quit_to_launcher)
    button_c.irq(trigger=machine.Pin.IRQ_RISING, handler=quit_to_launcher)

    try:
        __import__(file)

    except ImportError:
        # If the app doesn't exist, notify the user
        warning(None, f"Could not launch: {file}")
        time.sleep(4.0)
    except Exception as e:
        # If the app throws an error, catch it and display!
        print(e)
        warning(None, str(e))
        time.sleep(4.0)

    # If the app exits or errors, do not relaunch!
    state_clear_running()
    machine.reset()  # Exit back to launcher


# Draw an overlay box with a given message within it
def warning(display, message, width=badger2040.WIDTH - 20, height=badger2040.HEIGHT - 20, line_spacing=20, text_size=0.6):
    print(message)

    if display is None:
        display = badger2040.Badger2040()
        display.led(128)

    # Draw a light grey background
    display.set_pen(12)
    display.rectangle((badger2040.WIDTH - width) // 2, (badger2040.HEIGHT - height) // 2, width, height)

    width -= 20
    height -= 20

    display.set_pen(15)
    display.rectangle((badger2040.WIDTH - width) // 2, (badger2040.HEIGHT - height) // 2, width, height)

    # Take the provided message and split it up into
    # lines that fit within the specified width
    words = message.split(" ")

    lines = []
    current_line = ""
    for word in words:
        if display.measure_text(current_line + word + " ", text_size) < width:
            current_line += word + " "
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    lines.append(current_line.strip())

    display.set_pen(0)

    # Display each line of text from the message, centre-aligned
    num_lines = len(lines)
    for i in range(num_lines):
        length = display.measure_text(lines[i], text_size)
        current_line = (i * line_spacing) - ((num_lines - 1) * line_spacing) // 2
        display.text(lines[i], (badger2040.WIDTH - length) // 2, (badger2040.HEIGHT // 2) + current_line, badger2040.WIDTH, text_size)

    display.update()
