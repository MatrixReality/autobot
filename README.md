Autobot

Raspberry Pi robot

Projeto em desenvolvimento, funcional na plataforma base. 
Preparando Gist com a montagem e makefile de instalação

Autostart:
    Dar permissão ao arquivo de autostart do projeto
    `sudo chmod 777 autobot.sh`

    Abrir o arquivo 
    `sudo nano /etc/xdg/lxsession/LXDE-pi/autostart`

    adicionar a seguinte linha no final do arquivo de autostart:
    `@/home/pi/Dev/autobot/autobot.sh`

Componentes:
    - [Plataforma Rocket-tank](https://www.robocore.net/robotica-robocore/plataforma-robotica-rocket-tank)
    - [Kit de expansão Rocket-tank](https://www.robocore.net/item-mecanico/kit-de-expansao-rocket-tank)
    - [Suporte pan tilt](https://lista.mercadolivre.com.br/suporte-pan-tilt-arduino)
    - [PowerBank](https://lista.mercadolivre.com.br/power-bank-inova)
    - [Raspberry py ModelB 3](https://lista.mercadolivre.com.br/raspberry-py-modelb-3)
    - [Raspicam](https://www.robocore.net/acessorios-raspberry-pi/camera-para-raspberry-pi-rev-1-3)
    - [Ponte H l298n](https://lista.mercadolivre.com.br/raspiberry-cam)
    - [Tela LCD i2c](https://lista.mercadolivre.com.br/tela-lcd-l2c)
    - [16 ch pwm](https://lista.mercadolivre.com.br/16-ch-pwm)

Referencias:
    - [Tela LCD i2c](https://github.com/the-raspberry-pi-guy/lcd)
    - [Ponte H l298n](https://sharad-rawat.medium.com/interfacing-l298n-h-bridge-motor-driver-with-raspberry-pi-7fd5cb3fa8e3)
    - [Controle por keypad](https://www.explainingcomputers.com/rasp_pi_robotics.html)
    - [Arduino pool de ultrassonico](https://www.arduinoecia.com.br/comunicacao-arduino-raspberry-pi-usando-i2c/)
    - [Arduino pool ultrassonico](https://imasters.com.br/back-end/arduino-e-raspberry-pi-trabalhando-juntos-parte-2-agora-com-i2c)
    - [Camera server](https://www.filipeflop.com/blog/streaming-com-raspberry-pi/)
    - [Explaining computers](https://www.explainingcomputers.com/pi_devastator_videos.html)
    - [Face Detection](https://learn.pimoroni.com/tutorial/electromechanical/building-a-pan-tilt-face-tracker)
    - [Multiples i2c IMPORTANT](https://medium.com/cemac/creating-multiple-i2c-ports-on-a-raspberry-pi-e31ce72a3eb2)
    - [Install Redis](https://amalgjose.com/2020/08/11/how-to-install-redis-in-raspberry-pi/)
