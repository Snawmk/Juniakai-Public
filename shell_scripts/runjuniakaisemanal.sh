#!/bin/bash
# executar esse script uma vez por semana
cd /home/ubuntu/Juniakai
python3 niver.py >> /home/ubuntu/cron.log
python3 ativos.py >> /home/ubuntu/cron.log