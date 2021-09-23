# ! /usr/bin/env python

import curses
import subprocess

from time import sleep

class keyboard:
    def __init__(self, status, robot, display, servo = None):
        self.status = status
        self.robot = robot
        self.display = display
        self.servo = servo

    def _kill_process(self, pid):
        subprocess.run([
                'kill',
                '{}'.format(pid)
            ])

    def start_controlling(self):
        status = self.status
        robot = self.robot
        display = self.display
        servo = self.servo

        screen = curses.initscr()
        curses.noecho() 
        curses.cbreak()
        screen.keypad(True)

        display.print(status.msg_display, 2)

        try:
            while True:
                if not status.in_move and status.msg_display != status.old_msg_display:
                    display.print(status.msg_display, 2)

                char = screen.getch()

                if char == ord('q'):
                    display.print("     OUT  OF    ", 1)
                    display.print("     PROGRAM    ", 2)
                    '''
                    if HAS_CAM and is_cam_record:
                        camera.stop_recording()
                    '''
                    servo.camera_initial_position()

                    if status.redis_server_pid is not None:
                        self._kill_process(status.redis_server_pid)

                    if status.redis_server_pid is not None:
                        self._kill_process(status.redis_server_pid)

                    if status.socket_server_pid is not None:
                        self._kill_process(status.socket_server_pid)

                    #kill sonar thread
                    #sleep(0.05)
                    #raise KeyboardInterrupt
                    break

                elif servo is not None and char in [ord('w'), ord('a'), ord('s'), ord('d'), ord('x')]:
                    servo.camera_move(char)

                elif char == curses.KEY_UP:
                    if not status.colission_detected:
                        status.in_move = True
                        robot.forward()
                        status.direction = "Front"
                        display.print(status.direction, 2)
                    elif status.colission_detected and status.colission_string is not None:
                        display.print(status.colission_string, 2)
                    
                elif char == curses.KEY_DOWN:
                    status.in_move = True
                    robot.backward()
                    status.direction = "Back"
                    display.print(status.direction, 2)                

                elif char == curses.KEY_RIGHT:
                    status.in_move = True
                    robot.right()
                    status.direction = "Right"
                    display.print(status.direction, 2)

                elif char == curses.KEY_LEFT:
                    status.in_move = True
                    robot.left()
                    status.direction = "Left"
                    display.print(status.direction, 2)

                elif char == 10:
                    status.msg_display = "Use arrow keys"
                    display.print(status.msg_display, 2)
                    status.in_move = False
                    status.direction = None
                    robot.stop()

                elif char == ord('m'):
                    result = subprocess.run(['vcgencmd', 'measure_temp'], stdout=subprocess.PIPE)
                    cpu_temp = str(result.stdout)
                    status.old_msg = status.msg_display
                    status.msg_display = "cpu {} c".format(cpu_temp[2:(len(cpu_temp)-5)])
                    display.print(status.msg_display, 2)

                    sleep(1.5)
                    status.msg_display = status.old_msg

                elif char == ord('t'):
                    status.msg_display = "Test pan & tilt"
                    display.print(status.msg_display, 2)
                    servo.test_pan_tilt()

                else:
                    display.print("<< wrong data >>", 2)
                    sleep(1)

        finally:
            #Close down curses properly, inc turn echo back on!
            curses.nocbreak(); screen.keypad(0); curses.echo()
            curses.endwin()
