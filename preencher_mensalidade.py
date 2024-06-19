#!/bin/env python3
from datetime import datetime
import pandas as pd
from functions import entrar_planilha, get_google_sheet, discord_webhook_table,discord_webhook, get_row, get_days_until, print_last_month
import time

# Este script irá ler a planilha Departamento de Jovens e irá popular a aba de mensalidade
# com as pessoas que estão devendo no mês anterior
# Rodar esse script 1 vez ao mês.

# Conectar na planilha do Departamento de Jovens
ws = entrar_planilha('Departamento de Jovens','Mensalidade')
# Pegar os valores da planilha numa tabela
records_data = get_google_sheet('Departamento de Jovens','Mensalidade')

# convert the json to dataframe
mensalidade_df = pd.DataFrame.from_dict(records_data)

# Pega a primeira linha da planilha
row = get_row('Departamento de Jovens','Mensalidade',1)

# retira as primeiras entradas da lista para ter apenas as datas
for i in range(9):
    row.pop(0)

# define a data atual
data_atual = datetime.today().date()
data_atual_txt = data_atual.strftime("%d/%m/%Y")

# Lista com cont de dias de cada mês
lista_dias = []
for i in row:
    linha = datetime.strptime(i,"%d/%m/%Y").date()
    bday_days = get_days_until(linha,data_atual)
    lista_dias.append(bday_days)

# Descobre o primeiro index positivo e quando achar, subtrai-se 1 para descobrir o último negativo da lista
index_este_mes = 0
for i in lista_dias:
    if i <= 0:
        index_este_mes = index_este_mes + 1
    else:
        index_este_mes = index_este_mes - 1
        break

# definição de var para o index do mês passado
index_mes_passado = index_este_mes - 1
mes_passado = row[index_mes_passado]

# drop row 0 da mensalidade_df[row[index]]
mensalidade_df = mensalidade_df.drop(mensalidade_df.index[0])

# filtrar membros ATIVOS
ativos_df = mensalidade_df.loc[mensalidade_df['Status'] == 'ATIVO']

# filtrar apenas membros que pagam mensalidade, dropando os que tem plano de R$ 0,00
# ativos_pagantes_df = ativos_df.drop(ativos_df[ativos_df['Mensalidade'] == 'R$ 0,00'].index)
ativos_pagantes_df = ativos_df
ativos_pagantes_df.drop(ativos_pagantes_df[ativos_pagantes_df['Mensalidade'] == ""].index)

# cria lista com nome e coluna do mês atual
nome = list(ativos_pagantes_df["Nome"])
mensalidade_atual = list(ativos_pagantes_df["Mensalidade"])
lista_mes_passado = list(ativos_pagantes_df[mes_passado])
nome_mes = list(zip(nome, mensalidade_atual, lista_mes_passado))

# procura na planilha onde está a celula do mês passado
cell_mes_passado = ws.find(mes_passado)
row_mes_passado = cell_mes_passado.row
col_mes_passado = cell_mes_passado.col

# percorrer a lista lista_mes_passado e onde estiver com valor vazio, preencher com o valor devido
# Aproveitando e add Lista dos Pagantes do mês + Lista dos não pagantes do mês
lista_pagantes_do_mes = []
lista_devedores_do_mes = []
idx = 0
for i in lista_mes_passado:
    time.sleep(3)
    if i == "":
        cell_nome = ws.find(nome_mes[idx][0])
        row_cell_nome = cell_nome.row
        valor_devido_str = ws.cell(row_cell_nome, 7).value
        if bool(valor_devido_str) == True:
            if (valor_devido_str != "R$ 0,00"):
                lista_devedores_do_mes.append(nome_mes[idx][0])
            if len(valor_devido_str) == 8:
                valor_devido = int(valor_devido_str[3] + valor_devido_str[4])*-1
            if len(valor_devido_str) == 7:
                valor_devido = int(valor_devido_str[3])*-1
            ws.update_cell(row_cell_nome,col_mes_passado,valor_devido)
            idx = idx + 1
        if bool(valor_devido_str) == False:
            error = True
            break
    if i == "-":
        idx = idx + 1
        pass
    if (i != "" and i != "-"):
        lista_pagantes_do_mes.append(nome_mes[idx][0])
        idx = idx + 1
        pass

# Caso uma das listas esteja vazia, é adicionado um valor "-"
if len(lista_devedores_do_mes) == 0:
    lista_devedores_do_mes.append("-")
if len(lista_pagantes_do_mes) == 0:
    lista_pagantes_do_mes.append("-")

# chama função para receber o nome do mes passado
mespassado_string = print_last_month()

# quantidade de plano Juniakai
qtd_plano_juniakai = len(ativos_pagantes_df["Nome"])

# output do código em formato de mensagem do discord
msg1 = ""
msg2 = ""
if error == False:
    msg = f"Resumo da mensalidade do mês de {mespassado_string} \nTotal de pessoaas que deveriam pagar no mes: {qtd_plano_juniakai}"
    for i in range(len(lista_pagantes_do_mes)):
        msg1 = msg1 + f"{lista_pagantes_do_mes[i]} \n"
    for i in range(len(lista_devedores_do_mes)):
        msg2 = msg2 + f"{lista_devedores_do_mes[i]} \n"
else:
    msg = "Erro! Provavelmente está faltando adicionar o plano de pagamento da mensalidade (JOVENS ou SECRETARIA) em algum dos ATIVOS! Favor verificar."

# Declaração dos parâmetros do Bot
if error == False:
    bot = {
        'webhook_url':'https://discord.com/api/webhooks/954242082288066580/jJVdVkn6A44yn_I5Dy7HI4xbJ0-atcZR645KJm5GyEw9qqrNkvNGsvLDdR-O4GGqre2n',
        'title_msg':f'MENSALIDADE - Mes {mespassado_string} de {datetime.now().year}',
        'msg':msg,
        'color':'0x2e702a',
        'name_author':'Sr. Barriga - Planilha Departamento de Jovens',
        'author_icon':'https://pbs.twimg.com/profile_images/322956481/srbarriga_400x400.jpg',
        'Field1':f'Pagantes do mes:',
        'txt_Field1':msg1,
        'Field2':f'Não pagantes do mes:',
        'txt_Field2':msg2,
        'thumb':'',
        'footer':'Sr. Barriga'}
    
    # Chama a função para mandar a mensagem no bot
    discord_webhook_table(bot)

else:
    bot = {
        'webhook_url':'https://discord.com/api/webhooks/954242082288066580/jJVdVkn6A44yn_I5Dy7HI4xbJ0-atcZR645KJm5GyEw9qqrNkvNGsvLDdR-O4GGqre2n',
        'title_msg':f'MENSALIDADE - Mes {mespassado_string} de {datetime.now().year}',
        'msg':msg,
        'color':'0x2e702a',
        'name_author':'Sr. Barriga - Planilha Departamento de Jovens',
        'author_icon':'https://pbs.twimg.com/profile_images/322956481/srbarriga_400x400.jpg',
        'thumb':'',
        'footer':'Sr. Barriga'}
    
    # Chama a função para mandar a mensagem no bot
    discord_webhook(bot)