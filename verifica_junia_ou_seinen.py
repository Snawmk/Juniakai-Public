#!/bin/env python3
from functions import entrar_planilha, get_google_sheet, discord_webhook, discord_webhook_table3, discord_webhook_table
from datetime import datetime
import pandas as pd

# Este código irá verificar a lista de ativos na tabela MASTER DATABASE da planilha de Jovens e irá atualizar nos cadastros quem é JUNIA e quem é SEINEN baseado na idade de cada um
# Os coordenadores serão exceção a essa regra e o script irá avisar quem fará 18 anos no ano vigente

# Definição da lista de Coordenadores que serão exceção
coord = [
    "Alexandre Marques Yamaguishi",
    "Danilo Gama Alves",
    "Guilherme Augusto Marcelino",
    "Pedro Takeshi Odo Lopes",
    "Wellinghton Akira Komiyama"
]
# Definção da idade limite para separar quem é JUNIA de quem é SEINEN
idade_limite = 18

# Dicionario de nome e idade
NomeIdadeDict = {}

# Lista de Junias
lista_Junia = []

# Lista de Seinens
lista_Seinen = []

# Lista de pessoas que estão sem idade na planilha MASTER DATABASE
lista_idade_zerada =[]

# Lista de jovens com 17 anos
dezesseteanos = []

# Conectar na planilha do Departamento de Jovens
ws = entrar_planilha('Departamento de Jovens','Master Database')

# Conectar na planilha do Departamento de Jovens
records_data = get_google_sheet('Departamento de Jovens','Master Database')

# convert the json to dataframe
cadastro_df = pd.DataFrame.from_dict(records_data)

# filtrar planilha de presença para apenas pessoas ativas
cadastro_df = cadastro_df.loc[cadastro_df['Status'] == 'ATIVO']

# Criar um dicionario de chave e valor
keys = list(cadastro_df["Nome"])
values = list(cadastro_df["Idade"])

# Loop para zerar as strings vazias 
contador = 0
for idade in values:
    if idade == "":
        values[contador] = 0
    contador += 1

# Zip das duas listas em um dicionário
NomeIdadeDict = dict(zip(keys,values))

# Criar lista separada para JUNIAS e SEINENS
for nome in NomeIdadeDict:
    if nome in coord:
        continue
    else:
        if int(NomeIdadeDict[nome]) >= idade_limite:
            lista_Seinen.append(nome)
        elif int(NomeIdadeDict[nome]) == 0:
            lista_idade_zerada.append(nome)
            erro = True
        else:
            lista_Junia.append(nome)
            if int(NomeIdadeDict[nome]) == 17:
                dezesseteanos.append(nome)
   
# Loop para procurar o nome da pessoa na lista_Junia e escreve na MASTER DATABASE o valor 'Junia'
for nome in lista_Junia:
    if nome in coord:
        continue
    else:
        busca = ws.find(nome)
        ws.update_cell(busca.row,4,"Junia")

# Loop para procurar o nome da pessoa na lista_Junia e escreve na MASTER DATABASE o valor 'Seinen'
for nome in lista_Seinen:
    if nome in coord:
        continue
    else:
        busca = ws.find(nome)
        ws.update_cell(busca.row,4,"Seinen")

msg = "Lista JUNIAS e SEINENS Ativos: "
msg1 = ""
msg2 = ""
msg3 = ""

# Declaração dos parâmetros do Bot

for i in range(len(lista_Junia)):
    msg1 = msg1 + f"{lista_Junia[i]} \n"
    
for i in range(len(lista_Seinen)):
    msg2 = msg1 + f"{lista_Seinen[i]} \n"

for i in range(len(lista_idade_zerada)):
    msg3 = msg3 + f"{lista_idade_zerada[i]} \n"

if erro == True: 
    bot = {
        'webhook_url':'https://discord.com/api/webhooks/950961251574480986/Mvd2mEAAN13ie3gwsMBKBlXC6CetOyKwDEBwSnDuW6UWuGeq6FUu7yPdHj8CVYPlPWmw',
        'title_msg':"Verificação da CLASSIFICAÇÃO entre JUNIA e SEINEN's",
        'msg':msg,
        'color':'0xff0000',
        'name_author':'Sr. chekas - Planilha Departamento de Jovenss',
        'author_icon':'https://cdn-icons-png.flaticon.com/512/11879/11879749.png',
        'Field1':f'JUNIAS: {len(lista_Junia)}',
        'txt_Field1':msg1,
        'Field2':f'SEINEN: {len(lista_Seinen)}',
        'txt_Field2':msg2,
        'Field3':f"Existem {len(lista_idade_zerada)} jovens sem a data de nascimento cadastrada! Favor verificar!",
        'txt_Field3':msg3,
        'thumb':'',
        'footer':'Sr. chekas'}
    
    # Chama a função para mandar a mensagem no bot
    discord_webhook_table3(bot)

else:
    bot = {
        'webhook_url':'https://discord.com/api/webhooks/950961251574480986/Mvd2mEAAN13ie3gwsMBKBlXC6CetOyKwDEBwSnDuW6UWuGeq6FUu7yPdHj8CVYPlPWmw',
        'title_msg':"Verificação da CLASSIFICAÇÃO entre JUNIA e SEINEN's",
        'msg':msg,
        'color':'0x000080',
        'name_author':'Sr. chekas - Planilha Departamento de Jovenss',
        'author_icon':'https://cdn-icons-png.flaticon.com/512/11879/11879749.png',
        'Field1':f'JUNIAS: {len(lista_Junia)}',
        'txt_Field1':msg1,
        'Field2':f'SEINEN: {len(lista_Seinen)}',
        'txt_Field2':msg2,
        'thumb':'',
        'footer':'Sr. chekas'}
    # Chama a função para mandar a mensagem no bot
    discord_webhook_table(bot)

msg = ""
busca_niver = []
for junia in dezesseteanos:
    busca_niver_cell = ws.find(junia)
    busca_niver_row = busca_niver_cell.row
    niver = ws.cell(busca_niver_row,7).value
    if niver == None:
         niver = "Falta Cadastrar!"
    busca_niver.append(niver)

for i in range(len(dezesseteanos)):
    msg = msg + f"{dezesseteanos[i]} - " + busca_niver[i] + '\n'
bot = {
    'webhook_url':'https://discord.com/api/webhooks/950961251574480986/Mvd2mEAAN13ie3gwsMBKBlXC6CetOyKwDEBwSnDuW6UWuGeq6FUu7yPdHj8CVYPlPWmw',
    'title_msg':f"ATENÇÃO: Lista de Pessoas que estão com {idade_limite-1} anos",
    'msg':msg,
    'color':'0xff0000',
    'name_author':'Sr. chekas - Planilha Departamento de Jovens',
    'author_icon':'https://cdn-icons-png.flaticon.com/512/11879/11879749.png',
    'thumb':'',
    'footer':'Sr. chekas'}
    
    # Chama a função para mandar a mensagem no bot
discord_webhook(bot)