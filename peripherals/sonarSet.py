# ! /usr/bin/env python

import json
import smbus

from time import sleep

LOG_COLISSION = True
LIMIT_COLISSION_IN_CM = 15

ARDUINO_SONAR_SET_BUS = 2
ARDUINO_SONAR_SET_ADDR = 0x18

class sonarSet:
    def __init__(self, status, robot, queue = None, bus = None, addr = None):
        self.status = status
        self.robot = robot
        self.queue = queue

        self.bus = bus
        if bus is None:
            self.bus = ARDUINO_SONAR_SET_BUS

        self.addr = addr
        if addr is None:
            self.addr = ARDUINO_SONAR_SET_ADDR

        self.i2c_interface = smbus.SMBus(self.bus)


    def _get_data(self, last_distance):
        try:
            sonar_data_from_arduino = self.i2c_interface.read_i2c_block_data(self.addr, 0, 32)
            sonar_data = ''
            for i in range(len(sonar_data_from_arduino)):
                sonar_data += chr(sonar_data_from_arduino[i])
        
            return str(sonar_data)
        except:
            if last_distance is not None:
                return '{},00.00,00.00,00.00, '.format(last_distance)

    def worker(self):
        status = self.status
        log_colission = LOG_COLISSION
        limit = LIMIT_COLISSION_IN_CM

        last_sonar_data = None
        sonar_keys = ("center", "centerRight", "back", "centerLeft")

        while True:
            try:
                sonar_data = self._get_data(last_sonar_data)
                sonar_data =  sonar_data.split(",")
                del(sonar_data[len(sonar_data)-1])

                sonar_data = dict(zip(sonar_keys, sonar_data))

                if float(sonar_data["center"]) <= limit and not status.colission_detected and status.direction == "Front":
                    self.robot.stop()
                    status.colission_detected = True
                    if log_colission:
                        status.colission_string = 'STOP CRASH {}'.format(sonar_data["center"])

                elif status.colission_detected and status.direction != "Front":
                    status.colission_detected = False
                    if log_colission:
                        status.colission_string ='RETURN {}'.format(sonar_data["center"])

                if self.queue is not None:
                    key = "distance_log"
                    msg = {
                        "type": "distanceLog", 
                        "contents": sonar_data
                    }
                    self.queue.set(key, json.dumps(msg))

                if self.status is not None:
                    self.status.sonar_data = sonar_data
            
            except:
                #print("sonar failure")
                sonar_data = last_sonar_data

            sleep(0.10)
