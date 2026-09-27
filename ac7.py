X_SENSITIVITY = 0.5
Y_SENSITIVITY = 1.5


def update():
    yaw = filters.mapRange(trackIR.yaw, -70, 70, -vJoy[0].axisMax, vJoy[0].axisMax)
    pitch = filters.mapRange(trackIR.pitch, -70, 70, -vJoy[0].axisMax, vJoy[0].axisMax)
    vJoy[0].x = yaw * X_SENSITIVITY
    vJoy[0].y = -pitch * Y_SENSITIVITY


stick = joystick["R-VPC CDT-AEROMAX"]
throttle = joystick["VPC CDT-VMAX Throttle"]
pedals = joystick["VPC R1-FALCON Pedals"]

throttle_position = max(0.0, min(1.0, (throttle.xRotation + 1000.0) / 2000.0))
stick_position = max(0.0, min(1.0, (stick.zRotation + 1000.0) / 2000.0))

throttle_up = max(0.0, throttle_position - 0.5)
throttle_down = stick_position * 0.5
combined = max(0.0, min(1.0, 0.5 + throttle_up - throttle_down))

throttle_output = int((combined * 2.0 - 1.0) * vJoy[0].axisMax)
diagnostics.watch("throttle.xRotation=%d stick.zRotation=%d combined=%.3f vJoy.z=%d" %
                  (throttle.xRotation, stick.zRotation, combined, throttle_output))
vJoy[0].z = throttle_output

vJoy[0].rz = int(pedals.z * vJoy[0].axisMax / 1000)

if starting:
    stick.setRange(-1000, 1000)
    throttle.setRange(-1000, 1000)
    pedals.setRange(-1000, 1000)
    trackIR.update += update
