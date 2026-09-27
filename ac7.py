X_SENSITIVITY = 0.5
Y_SENSITIVITY = 1.5
PEDAL_DEADZONE = 50


def update():
    yaw = filters.mapRange(trackIR.yaw, -70, 70, -vJoy[0].axisMax, vJoy[0].axisMax)
    pitch = filters.mapRange(trackIR.pitch, -70, 70, -vJoy[0].axisMax, vJoy[0].axisMax)
    vJoy[0].x = yaw * X_SENSITIVITY
    vJoy[0].y = -pitch * Y_SENSITIVITY


stick = joystick["R-VPC CDT-AEROMAX"]
throttle = joystick["VPC CDT-VMAX Throttle"]
pedals = joystick["VPC R1-FALCON Pedals"]

throttle_up = (throttle.x + 1.0) / 2.0
throttle_down = (stick.z + 1.0) / 2.0

combined = throttle_up - throttle_down
combined = max(-1.0, min(1.0, combined))

vJoy[0].z = int(combined * vJoy[0].axisMax)

pedal_axis = pedals.x
vJoy[0].setButton(0, pedal_axis < -PEDAL_DEADZONE)
vJoy[0].setButton(1, pedal_axis > PEDAL_DEADZONE)

if starting:
    pedals.setRange(-1000, 1000)
    trackIR.update += update
