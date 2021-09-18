#! /usr/bin/env python

class robotStatus:
    __shared_instance = None

    redis_server_pid = None
    socket_server_pid = None
    http_server_pid = None

    in_move = False
    direction = None

    msg_display = None
    old_msg_display = None

    sonar_data = None
    colission_string = None
    colission_detected = False

    camera_pan = None
    camera_tilt = None

    def __init__(self):
        if robotStatus.__shared_instance is not None:
            raise Exception("This class is singleton class")
        else:
            robotStatus.__shared_instance = self

    @staticmethod
    def get_instance():
        if robotStatus.__shared_instance is None:
            robotStatus()

        return robotStatus.__shared_instance
    