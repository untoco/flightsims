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

throttle_output = int(throttle.xRotation * vJoy[0].axisMax / 1000)
deceleration_output = int(stick.zRotation * vJoy[0].axisMax / 1000)
diagnostics.watch(throttle.xRotation)
diagnostics.watch(stick.zRotation)
diagnostics.watch(throttle_output)
diagnostics.watch(deceleration_output)
vJoy[0].z = throttle_output
vJoy[0].rx = deceleration_output

vJoy[0].rz = int(pedals.z * vJoy[0].axisMax / 1000)

if starting:
    stick.setRange(-1000, 1000)
    throttle.setRange(-1000, 1000)
    pedals.setRange(-1000, 1000)
    trackIR.update += update
