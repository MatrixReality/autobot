#!/bin/bash
# This script is referred in the end of autostart file:
# sudo nano /etc/xdg/lxsession/LXDE-pi/autostart

echo "     "
echo "     "
echo "     8eeee8                                      "
echo "     8    8 e   e eeeee eeeee eeeee  eeeee eeeee "
echo "     8eeee8 8   8   8   8  88 8   8  8  88   8   "
echo "     88   8 8e  8   8e  8   8 8eee8e 8   8   8e  "
echo "     88   8 88  8   88  8   8 88   8 8   8   88  "
echo "     88   8 88ee8   88  8eee8 88eee8 8eee8   88  "
echo "     "
echo "     "

VERSION="v1.3"
REDIS_FOLDER="./bin"
VENV_PYTHON3="./venv/bin/python3"

cd /

echo "ver.: $VERSION"
echo "Keep wait for initialize all dependencies"
echo "..." 
echo ""

sleep 7.5

#transform gpio pins into i2c pins to arduino comunicates
echo "Prepare Sonar set Arduino i2c Pins"
sudo dtoverlay i2c-gpio bus=2 i2c_gpio_sda=12 i2c_gpio_scl=13
echo "Done!"
echo "-------------------------------------"

#transform gpio pins into i2c pins to lcd display comunicates
echo "Prepare LCD i2c Pins"
sudo dtoverlay i2c-gpio bus=3 i2c_gpio_sda=06 i2c_gpio_scl=07
echo "Done!"
echo "-------------------------------------"

cd /
cd /home/pi/Dev/autobot

#iniciate redis dependency to message broker
echo "Initialize Redis Server"
$(./bin/redis-server)&
REDIS_SERVER_PID=$!
echo "Redis Server on Pid: $REDIS_SERVER_PID Done!"
echo "-------------------------------------"
sleep 2.5

cd /
cd /home/pi/Dev/autobot/servers

#iniciate socket server to message broker
echo "Initialize Websocket Python Server"
$(.$VENV_PYTHON3 socket_server.py  -t socket_server)&
WEBSOCKET_SERVER_PID=$!
echo "Websocket Python Server on Pid: $WEBSOCKET_SERVER_PID Done!"
echo "-------------------------------------"
sleep 2.6

#iniciate stream cam client (consume messages and view robot cam)
echo "Initialize Http and Stream Python Server"
$(.$VENV_PYTHON3 stream_cam_socket.py $VERSION -t stream_server)&
HTTP_SERVER_PID=$!
echo "Http and Stream Python Server on Pid: $HTTP_SERVER_PID Done!"
echo "-------------------------------------"
sleep 2.5

cd /
cd /home/pi/Dev/autobot

#iniciate autobot control script
echo "Setting Autobot"
lxterminal -e $VENV_PYTHON3 autobot.py $VERSION $REDIS_SERVER_PID $WEBSOCKET_SERVER_PID $HTTP_SERVER_PID && echo "Autobot $VERSION Done in another terminal" && exit 0 && cd /
