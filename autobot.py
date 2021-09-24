#! /usr/bin/env python

import sys
import threading
import redis

from gpiozero import Robot
from dotenv import dotenv_values

from peripherals import robotStatus, lcdMonitor, sonarSet, keyboard, servoKit


class Autobot:
    def __init__(self, robot_motors = None, message_queue = None, display = None, sonar_set = None,  servo_kit = None):
        config = dotenv_values(".env")

        VERSION = "AUTOBOT    {}".format(config["VERSION"])
        DEV = config["DEV"].lower() in ('true', '1', 't')
        HAS_SERVO_KIT = config["HAS_SERVO_KIT"].lower() in ('true', '1', 't')
        HAS_ARDUINO_SONAR_SET = config["HAS_ARDUINO_SONAR_SET"].lower() in ('true', '1', 't')
        HAS_DISPLAY_LCD = config["HAS_DISPLAY_LCD"].lower() in ('true', '1', 't')
        HAS_MESSAGE_QUEUE = config["HAS_MESSAGE_QUEUE"].lower() in ('true', '1', 't')

        HOST_REDIS = config["HOST_REDIS"]
        PORT_REDIS = config["PORT_REDIS"]

        status = robotStatus()
        status.msg_display = "Use arrow keys"

        redis_server_pid = None
        socket_server_pid = None
        http_server_pid = None
        try:
            redis_server_pid = sys.argv[1]
            socket_server_pid = sys.argv[2]
            http_server_pid = sys.argv[3]
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
                display = lcdMonitor(config, message_queue)

                #pids = "{}, {}, {}".format(redis_server_pid, socket_server_pid, http_server_pid)
                #print(pids)
                #display.print(pids, 1)
                display.print(VERSION, 1)


        sonar_thread = None
        if HAS_ARDUINO_SONAR_SET:
            if sonar_set is None:
                sonar_set = sonarSet(config, status, robot_motors, message_queue)

            sonar_thread = threading.Thread(target=sonar_set.worker)
            sonar_thread.start()

        if HAS_SERVO_KIT:
            if servo_kit is None:
                servo_kit = servoKit(config, status)
        else:
            servo_kit = None

        keypad = keyboard(status, robot_motors, display, servo_kit)
        keypad.start_controlling() #run forever

autobot = Autobot()
