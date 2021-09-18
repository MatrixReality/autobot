#! /usr/bin/env python

import sys
import threading
import redis

from gpiozero import Robot

from peripherals import robotStatus, lcdMonitor, sonarSet, keyboard, servoKit

VERSION = "AUTOBOT    {}".format(sys.argv[1])

DEV = True
HAS_SERVO_KIT = True
HAS_ARDUINO_SONAR_SET = True
HAS_DISPLAY_LCD= True
HAS_MESSAGE_QUEUE=True

HOST_REDIS='localhost'
PORT_REDIS=6379

class Autobot:
    def __init__(self, robot_motors = None, message_queue = None, display = None, sonar_set = None,  servo_kit = None):
        status = robotStatus()
        status.msg_display = "Use arrow keys"

        redis_server_pid = None
        socket_server_pid = None
        http_server_pid = None
        try:
            redis_server_pid = sys.argv[2]
            socket_server_pid = sys.argv[3]
            http_server_pid = sys.argv[4]
        except:
            pass

        status.redis_server_pid = redis_server_pid 
        status.socket_server_pid = socket_server_pid
        status.http_server_pid = http_server_pid

        if robot_motors is None:
            #TODO remove magic numbers
            robot_motors = Robot(left=(22,17), right=(23, 24))

        if HAS_MESSAGE_QUEUE:
            if message_queue is None:
                #TODO Create wrapper to message queue, use MQTT or NSQ
                message_queue = redis.StrictRedis(host=HOST_REDIS, port=PORT_REDIS, db=0)

        if HAS_DISPLAY_LCD:
            if display is None:
                display = lcdMonitor(message_queue)

                #pids = "{}, {}, {}".format(redis_server_pid, socket_server_pid, http_server_pid)
                #print(pids)
                #display.print(pids, 1)
                display.print(VERSION, 1)


        sonar_thread = None
        if HAS_ARDUINO_SONAR_SET:
            if sonar_set is None:
                sonar_set = sonarSet(status, robot_motors, message_queue)

            sonar_thread = threading.Thread(target=sonar_set.worker)
            sonar_thread.start()

        if HAS_SERVO_KIT:
            if servo_kit is None:
                servo_kit = servoKit(status)
        else:
            servo_kit = None

        keypad = keyboard(status, robot_motors, display, servo_kit)
        keypad.start_controlling() #run forever

autobot = Autobot()