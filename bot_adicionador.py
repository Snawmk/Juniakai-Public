#!/bin/env python3
from functions import entrar_planilha, get_google_sheet, discord_webhook
import pandas as pd
import numpy as np
import time

# Este programa irá conectar na planilha de respostas ao formulário de cadastro do Juniakai e irá popular automaticamente os novos cadastros na Master Database presente na planilha 'Depatartamento dos Jovens'
# Conectar na planilha do Departamento de Jovens
ws = entrar_planilha('Departamento de Jovens','Master Database')

# Conectar na planilha Departamento de Jovens e obtem as respostas do formulario de cadastros
records_data_respostas = get_google_sheet('Departamento de Jovens','Respostas')
records_data_master = get_google_sheet('Departamento de Jovens','Master Database')

# convert the json to dataframe
respostas_df = pd.DataFrame.from_dict(records_data_respostas)
master_df = pd.DataFrame.from_dict(records_data_master)

# filtrar Master Database tirando os valores vazios
master_df_filtrado = master_df['Nome'].replace('', np.nan)
master_df_filtrado.dropna(inplace=True)

# Cria duas listas para receber os valores dos nomes cadastrados pelo Google Forms, e uma lista dos nomes cadastrados no Master Database
lista_respostas = list(respostas_df['Nome Completo do jovem (sem abreviações)'])
lista_master = list(master_df_filtrado)

# Variável que controlará se houve um update ou não
update = False

# Iteração da lista de respostas ao Google Forms para retirar '.' e espaços em branco
for i in range(len(lista_respostas)):
    lista_respostas[i] = lista_respostas[i].replace('.','').strip().upper()

# Iteração da lista de nomes no Master Database para retirar '.' e espaços em branco
for k in range(len(lista_master)):
    lista_master[k] = lista_master[k].replace('.','').strip().upper()

# Mapeamento das colunas na planilha de ORIGEM - Respostas
indice_col_org = {
    'Nome': 2,
    'Apelido': 3,
    'Celular': 4, 
    'Nasc': 5, 
    'Bairro': 7, 
    'Resp': 8,
    'Contato': 9,
    'Convenio': 10, 
    'Medic': 11, 
    'Entrada':12,
    'Obs':13
}

# Mapeamento das colunas na planilha de DESTINO - Master Database
indice_col_dst = {
    'Nome': 2,
    'Apelido': 3,
    'Celular': 6, 
    'Nasc': 7, 
    'Bairro': 9, 
    'Resp': 10,
    'Contato': 11,
    'Convenio': 12, 
    'Medic': 13, 
    'Entrada':14,
    'Obs':15
}

# Contador pra achar o a posição do novo cadastro
contador = 0

# Achar a próxima posição vazia na aba do Master Database
tamanho = len(master_df_filtrado)+1

#output do código em formato de mensagem do discord
msg = "Lista de novos Jovens que fizeram o cadastro no Formulario e foram inclusos na MASTER DATABASE: \n\n"

# Loop para comparar as pessoas do cadastro com a Master Database
for pessoa in lista_respostas:
    contador += 1
    if pessoa in lista_master:
        # Caso encontrar na lista da Master Database, skipa
        continue 
    else:
        msg = msg + pessoa + '\n'
        # Caso não encontrar, o proximo ID disponível será populado 
        cel_find = ws.find(str(tamanho))
        # Recebe a linha da planilha com o próx ID disponível
        cel_update_row = cel_find.row
        ws.update_cell(cel_update_row,5,"ATIVO")
        update = True
        
        # Popula a linha de ID disponível com os valores das colunas mapeadas nos dicionários 'indice_col_org' e 'indice_col_dst'
        for indice in indice_col_org:
            atualiza = respostas_df.iloc[contador-1][indice_col_org[indice]-1]
            ws.update_cell(cel_update_row,indice_col_dst[indice],atualiza)
        time.sleep(3)
        if int(ws.cell(cel_update_row,8).value) <= 17:
            juniaouSeinen = "Junia"
        else:
            juniaouSeinen = "Seinen"
        ws.update_cell(cel_update_row,4,juniaouSeinen)    
        tamanho = tamanho+1

# Decisão de enviar a mensagem ou não. Caso nada tenha sido adicionado, não enviar mensagem.
if update == True:
    # Declaração dos parâmetros do Bot
    bot = {
        'webhook_url':'https://discord.com/api/webhooks/950961251574480986/Mvd2mEAAN13ie3gwsMBKBlXC6CetOyKwDEBwSnDuW6UWuGeq6FUu7yPdHj8CVYPlPWmw',
        'title_msg':'Inclusão de NOVATOS na MASTER DATABASE',
        'msg':f'{msg}',
        'color':'0x000080',
        'name_author':'Sr. chekas - Planilha Departamento de Jovens',
        'author_icon':'https://cdn-icons-png.flaticon.com/512/11879/11879749.png',
        'thumb':'',
        'footer':'Sr. Chekas'}
    # Chama a função para mandar a mensagem no bot
    discord_webhook(bot)








