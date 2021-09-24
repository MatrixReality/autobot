# ! /usr/bin/env python

from time import sleep
from adafruit_servokit import ServoKit

class servoKit:
    def __init__(self, config, status = None, channels = None):
        self.status = status

        # Set channels to the number of servo channels on your kit.
        # 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
        if channels is None:
            channels = int(config["SERVO_KIT_CHANNELS"])

        kit = ServoKit(channels=channels)

        # Setting camera move controlling
        self.pan = kit.servo[0]
        self.tilt = kit.servo[1]

        self.pan_pos = {
            "center": 90,
            "left": 180,
            "right": 0
        }

        self.tilt_pos = {
            "base": 0,
            "medium1": 30,
            "medium2": 60,
            "top": 90,
            "horizon":130,
            "down": 180
        }

        self.camera_initial_position()
    
    def camera_initial_position(self):
        #_smooth_servo_angle_moviment(tilt, int(tilt.angle), tilt_pos["horizon"])
        #_smooth_servo_angle_moviment(pan, int(pan.angle), pan_pos["center"])
        status = self.status
        pan_pos = self.pan_pos
        tilt_pos = self.tilt_pos

        self.tilt.angle = tilt_pos["horizon"]
        self.pan.angle = pan_pos["center"]
        status.camera_tilt = tilt_pos["horizon"]
        status.camera_pan = pan_pos["center"]

    def camera_move(self, char):
        status = self.status
        pan_pos = self.pan_pos
        tilt_pos = self.tilt_pos
        pan_tilt_factor = int(30)

        try:
            if char == ord('w') or char == ord('s'):
                tilt_angle = int(status.camera_tilt)

                if char == ord('w'):
                    new_tilt = tilt_angle - pan_tilt_factor
                    if new_tilt < tilt_pos["base"]:
                        new_tilt = tilt_pos["base"]
                    self.tilt.angle = new_tilt


                elif char == ord('s'):
                    new_tilt = tilt_angle + pan_tilt_factor
                    if new_tilt > tilt_pos["down"]:
                        new_tilt = tilt_pos["down"]
                    self.tilt.angle = new_tilt

                status.camera_tilt = new_tilt

                #if new_tilt >= 0 or new_tilt <= 180:
                #    _smooth_servo_angle_moviment(tilt, tilt_angle, new_tilt)


            elif char == ord('a') or char == ord('d'):
                pan_angle = int(status.camera_pan)

                if char == ord('a'):
                    new_pan = pan_angle + pan_tilt_factor
                    if new_pan > pan_pos["left"]:
                        new_pan = pan_pos["left"]
                    self.pan.angle = new_pan

                elif char == ord('d'):
                    new_pan = pan_angle - pan_tilt_factor
                    if new_pan < pan_pos["right"]:
                        new_pan = pan_pos["right"]
                    self.pan.angle = new_pan

                status.camera_pan = new_pan

                #if new_pan >= 0 or new_pan <= 180:
                #    _smooth_servo_angle_moviment(pan, pan_angle, new_pan)

            elif char == ord('x'):
                self.camera_initial_position()

                #self.tilt.angle = tilt_pos["horizon"]
                #self.pan.angle = pan_pos["center"]
                #status.camera_tilt = tilt_pos["horizon"]
                #status.camera_pan = pan_pos["center"]

            #sleep(0.05)

        except:
            print("servoKit i2c except")
            pass


    def _smooth_servo_angle_moviment(servo, start_angle, end_angle):
        smooth_factor = 2
        v = int(pan_tilt_factor/smooth_factor)
        if end_angle > start_angle:
            for x in range(v):
                servo.angle += smooth_factor
                sleep(0.01)
        else:
            for x in range(v):
                servo.angle -= smooth_factor
                sleep(0.01)

    def test_pan_tilt(self):
        pan = self.pan
        tilt = self.tilt
        pan_pos = self.pan_pos
        tilt_pos = self.tilt_pos

        pan.angle = pan_pos["left"]
        sleep(0.5)
        pan.angle = pan_pos["right"]
        sleep(0.5)
        pan.angle = pan_pos["center"]
        sleep(0.5)

        tilt.angle = tilt_pos["base"]
        sleep(0.5)
        tilt.angle = tilt_pos["down"]
        sleep(0.5)
        tilt.angle = tilt_pos["horizon"]
