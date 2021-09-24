# Web streaming example
# Source code from the official PiCamera package
# http://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming

import io
import picamera
import logging
import socketserver
import sys
from http import server
from dotenv import dotenv_values
from threading import Condition

import asyncio
import datetime
import random
import websockets

VERSION = "AUTOBOT    {}".format(config["VERSION"])
WEBSOCKET_HOST = config["WEBSOCKET_HOST"]
WEBSOCKET_PORT = config["WEBSOCKET_PORT"]

PAGE="""\
<html>
    <head>
        <title>Raspberry Pi - Camera</title>
    </head>
    <body style="font-family:Arial;">
        <center><h1>Raspberry Pi - Camera</h1></center>
        <center>
            <div style="height:35px;width:200px;background-color:blue;color:white;">
    
                <span id="logLine01"></span><br/>
                <span id="logLine02"></span>
            </div>
        </center>
        <center>
        <table border="1" style="font-size:x-small">
            <tr>
                <td></td>
                <td id="center"></td>
                <td></td>
            <tr>
                <td id="centerLeft"></td>
                <td></td>
                <td id="centerRight"></td>
            <tr>
                <td colspan="3" align="center">Tank</td>
                        <tr>
                <td></td>
                <td id="back"></td>
                <td></td>
        </table>
        </center>
        <center><img src="stream.mjpg" width="640" height="480"></center>
    </body>
    <script>

        var logLine01 = document.getElementById('logLine01');
        var logLine02 = document.getElementById('logLine02');

        logLine01.innerHTML = '{}';
        logLine02.innerHTML = 'Use arrow keys' 

        var connection = new WebSocket('ws://{}:{}/websocket');
        connection.onopen = function(){{
            connection.send('ping');
        }};
        connection.onerror = function(error){{
            console.log('Websocket error '+error);
        }};
        connection.onmessage = function(e){{
            data = e.data;             
            data = data.replace("b'", "");
            data = data.replace("'", "");
            data = data.replace("b\\"", "");
            data = JSON.parse(data);
            
            if(data["type"] == "displayLog"){{
                el = document.getElementById("logLine0"+data["contents"]["line"])
                el.innerHTML = data["contents"]["message"];
            }} else if(data["type"]  == "distanceLog"){{
                for(const [key, value] of Object.entries(data["contents"])){{
                    document.getElementById(key).innerHTML=value;
                }}
            }}
        }};
    </script>
</html>
""".format(VERSION, WEBSOCKET_HOST, WEBSOCKET_PORT)

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

with picamera.PiCamera(resolution='640x480', framerate=30) as camera:
    output = StreamingOutput()
    #Uncomment the next line to change your Pi's Camera rotation (in degrees)
    #camera.rotation = 90
    camera.start_recording(output, format='mjpeg')
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()