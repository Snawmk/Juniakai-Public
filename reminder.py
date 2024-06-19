#!/bin/env python3
from functions import discord_webhook

# Declaração dos parâmetros do Bot
bot = {
    'webhook_url':'https://discord.com/api/webhooks/950961251574480986/Mvd2mEAAN13ie3gwsMBKBlXC6CetOyKwDEBwSnDuW6UWuGeq6FUu7yPdHj8CVYPlPWmw',
    'title_msg':'Checar Grupos Whatsapp: LEMBRETE',
    'msg':'Atenção Coordenadores!! \n Por favor exportar a lista do membros do Whatsapp ainda hoje e colocar no GITHUB JUNIAKAI!',
    'color':'0x781912',
    'name_author':'Sr. Chekas - Planilha Departamento de Jovens',
    'author_icon':'https://i.imgur.com/7XeLpEa.jpg',
    'thumb':'',
    'footer':'Sr. Chekas'}
# Chama a função para mandar a mensagem no bot
discord_webhook(bot)

