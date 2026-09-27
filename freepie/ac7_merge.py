# FreePIE / IronPython 2.7. Example: stick + throttle -> vJoy device 1.
# EDIT these indices after checking FreePIE Watch. Never select vJoy as input.
STICK = 0
THROTTLE = 1
USE_PEDALS = False
PEDALS = 2

# Physical joystick buttons are zero-based; vJoy setButton is also zero-based.
# Input.ini uses one-based Button numbers.
BUTTONS = (
    (STICK, 0, 0),    # trigger -> vJoy Button1: gun
    (STICK, 1, 1),    # stick button 2 -> Button2: missile
    (STICK, 2, 2),    # stick button 3 -> Button3: special weapon
    (STICK, 3, 3),    # stick button 4 -> Button4: target
    (THROTTLE, 0, 4), # throttle button 1 -> Button5: radar
    (THROTTLE, 1, 5), # throttle button 2 -> Button6: flare
)

SOURCE_MAX = 1000
DEADZONE = 30


def clamp(value, low, high):
    return max(low, min(high, value))


def centered(value):
    value = clamp(value, -SOURCE_MAX, SOURCE_MAX)
    if abs(value) <= DEADZONE:
        return 0
    if value > 0:
        return (value - DEADZONE) * SOURCE_MAX / (SOURCE_MAX - DEADZONE)
    return (value + DEADZONE) * SOURCE_MAX / (SOURCE_MAX - DEADZONE)


def output_axis(value):
    return int(clamp(value, -SOURCE_MAX, SOURCE_MAX) * vJoy[0].axisMax / SOURCE_MAX)


if starting:
    joystick[STICK].setRange(-SOURCE_MAX, SOURCE_MAX)
    joystick[THROTTLE].setRange(-SOURCE_MAX, SOURCE_MAX)
    if USE_PEDALS:
        joystick[PEDALS].setRange(-SOURCE_MAX, SOURCE_MAX)

# Assumed input axes: stick X=roll, Y=pitch, throttle Z=power.
# Change source properties if your hardware reports different axes.
vJoy[0].x = output_axis(centered(joystick[STICK].x))
vJoy[0].y = output_axis(centered(joystick[STICK].y))
vJoy[0].z = output_axis(joystick[THROTTLE].z)
if USE_PEDALS:
    vJoy[0].rz = output_axis(centered(joystick[PEDALS].x))
else:
    # Assumed twist grip for yaw. Replace .zRotation as needed.
    vJoy[0].rz = output_axis(centered(joystick[STICK].zRotation))

for source, physical_button, virtual_button in BUTTONS:
    vJoy[0].setButton(virtual_button, joystick[source].getDown(physical_button))
