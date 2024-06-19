#!/bin/bash
# executar esse script uma vez por mes, no dia 01
cd /home/ubuntu/Juniakai
python3 preencher_divida_nipo.py >> /home/ubuntu/cron.log
sleep 2m
python3 preencher_mensalidade.py >> /home/ubuntu/cron.log
sleep 2m
python3 mensalidade_atividades.py >> /home/ubuntu/cron.log