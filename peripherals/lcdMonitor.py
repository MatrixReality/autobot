# ! /usr/bin/env python

import json

from peripherals import drivers
from datetime import datetime

DISPLAY_LCD_BUS = 3
DISPLAY_LCD_ADDR = 0x27
DISPLAY_COLUMMS = 16

class lcdMonitor:
    def __init__(self, message_queue = None, display_columms = None, bus = None, addr = None):
        self.display_columms = display_columms
        if display_columms is None:
            self.display_columms = DISPLAY_COLUMMS

        self.bus = bus
        if bus is None:
            self.bus = DISPLAY_LCD_BUS

        self.addr = addr
        if addr is None:
            self.addr = DISPLAY_LCD_ADDR

        self.display_in_use = False
        self.message_queue = message_queue
        self.display = drivers.Lcd(self.addr, self.bus)

    def print(self, message = 'log', line = 1):
        try:
            if not self.display_in_use:
                self.display_in_use = True
                
                is_short_string = len(message) < self.display_columms
                if is_short_string:
                    message = message.ljust(self.display_columms, " ")
                    self.display.lcd_display_string(message, line)
                else:
                    self._display_long_string(message, line)
                
                self.display_in_use = False
        except:
            print("display_log except")
            #_restart_lcd()
            pass

        if self.message_queue is not None:
            msg = {
                "type": "displayLog", 
                "contents": {
                    "line":line, 
                    "message": message
                }
            }
            msg = json.dumps(msg)

            key = str(datetime.now().strftime('%d_%m_%Y_%H%M%S'))
            key = "display_log:{}".format(key)

            #TODO create wrapper redis as message broker interface
            self.message_queue.set(key, msg)

    def _display_long_string(self, text = '', num_line = 1): 
        if len(text) > self.display_columms:
            self.display.lcd_display_string(text[:self.display_columms], num_line)
            sleep(1)
            for i in range(len(text) - self.display_columms + 1):
                text_to_print = text[i:i+self.display_columms]
                self.display.lcd_display_string(text_to_print, num_line)
                sleep(0.2)
            sleep(1)
        else:
            self.display.lcd_display_string(text, num_line)


    def _restart_lcd():
        try:
            self.display_in_use = True
            self.display.lcd_clear()
            #self.display_log(VERSION, 1)
            self.display_in_use = False
        except:
            pass