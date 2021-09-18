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

VERSION="v1.0"
echo "ver.: $VERSION"
echo "Keep wait for initialize all dependencies"
echo "..." 
echo ""

cd /
sleep 10

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

#iniciate redis dependency to message broker
cd /home/pi/redis-6.0.6/src
echo "Initialize Redis Server"
$(./redis-server)&
REDIS_SERVER_PID=$!
echo "Redis Server on Pid: $REDIS_SERVER_PID Done!"
echo "-------------------------------------"
sleep 2.5

#iniciate socket server to message broker
cd /
cd /home/pi/Dev/autobot/servers
echo "Initialize Websocket Python Server"
$(python3 socket_server.py  -t socket_server)&
#lxterminal -e python3 socket_server.py -t socket_server
WEBSOCKET_SERVER_PID=$!
echo "Websocket Python Server on Pid: $WEBSOCKET_SERVER_PID Done!"
echo "-------------------------------------"
sleep 2.5

#iniciate stream cam client (consume messages and view robot cam)
echo "Initialize Http and Stream Python Server"
$(python3 stream_cam_socket.py $VERSION -t stream_server)&
#lxterminal -e python3 stream_cam_socket.py $VERSION -t stream_server
HTTP_SERVER_PID=$!
echo "Http and Stream Python Server on Pid: $HTTP_SERVER_PID Done!"
echo "-------------------------------------"
sleep 2.5

#iniciate autobot control script
cd ..
echo "Setting Autobot"
#$(python3 autobot.py $VERSION $REDIS_SERVER_PID $WEBSOCKET_SERVER_PID $HTTP_SERVER_PID -t autobot_controler)
lxterminal -e python3 autobot.py $VERSION $REDIS_SERVER_PID $WEBSOCKET_SERVER_PID $HTTP_SERVER_PID -t autobot_controler
echo "Autobot $VERSION"
echo "Done in another terminal!"
exit 0
cd /
