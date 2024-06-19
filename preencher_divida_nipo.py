#!/bin/env python3
from datetime import datetime
import pandas as pd
from functions import entrar_planilha, get_google_sheet, discord_webhook, get_row, get_days_until, print_last_month

# Este script irá ler a planilha Departamento de Jovens e irá na aba de mensalidade e Pagamentos Nipo
# Irá popular o controle de dívida ao Nipo mensalmente conforme o número de ativos que pagam mensalidade do Nipo para o Juniakai
# Rodar esse script 1 vez ao mês.

def preencher_divida(planilha, plano, cell, status, icon, aba_cadastro, col_ativo):
    # Conectar na planilha da atividade
    ws = entrar_planilha(planilha,'Pagamentos Nipo')
    # Pegar os valores da planilha numa tabela
    records_data = get_google_sheet(planilha,'Mensalidade')
    
    # convert the json to dataframe
    mensalidade_df = pd.DataFrame.from_dict(records_data)
    
    if (plano == "Juniakai"):
        # filtrar planilha de mensalidade para apenas pessoas ativas e com plano Juniakai
        ativos_df = mensalidade_df.loc[mensalidade_df[status] == 'ATIVO']
        ativos_df = ativos_df.loc[ativos_df['Plano'] == plano]

        # conta quantas pessoas são do plano Juniakai, ou seja, que pagam a parte do Nipo para nós
        qtd_plano_juniakai = len(ativos_df['Plano'])
    else:
        records_data_cadastro = get_google_sheet(planilha,aba_cadastro)
        cadastro_df = pd.DataFrame.from_dict(records_data_cadastro)
        ativos_df = cadastro_df.loc[cadastro_df[col_ativo] == 'ATIVO']
        ativos_df = ativos_df.loc[ativos_df['Associado Nipo'] == 'FALSE']

        # conta quantas pessoas são do plano Juniakai, ou seja, que pagam a parte do Nipo para nós
        qtd_plano_juniakai = len(ativos_df['Associado Nipo'])

    # # define lista de pessoas que devem pagar naquele mês em uma string
    # deveriam_pagar = ""
    # for i in ativos_df['Nome']:
    #     deveriam_pagar = deveriam_pagar + i + "\n"

    # lê o valor da mensalidade do Nipo preenchido na planilha, na aba Listas
    ws = entrar_planilha(planilha,'LISTAS')
    mensalidade_nipo_str = ws.acell(cell).value
    if len(mensalidade_nipo_str) == 8:
        mensalidade_nipo = int(mensalidade_nipo_str[3] + mensalidade_nipo_str[4])
    if len(mensalidade_nipo_str) == 7:
        mensalidade_nipo = int(mensalidade_nipo_str[3])


    # calcula quantidade * mensalidade do Nipo
    divida_atual = mensalidade_nipo * qtd_plano_juniakai

    # ler a planilha de controle
    ws = entrar_planilha(planilha,'Pagamentos Nipo')

    # define a data atual
    data_atual = datetime.today().date()
    data_atual_txt = data_atual.strftime("%d/%m/%Y")

    # Pega a primeira linha da planilha
    row = get_row(planilha,'Pagamentos Nipo',1)

    # Lista com cont de dias de cada mês
    lista_dias = []
    for i in row:
        if i == "":
            pass
        else:
            linha = datetime.strptime(i,"%d/%m/%Y").date()
            bday_days = get_days_until(linha,data_atual)
            lista_dias.append(bday_days)

    # descarta o primeiro valor da lista row com valor de "", para manter apenas as datas
    row.pop(0)

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

    # procura na planilha onde está a celula do mês passado
    cell_mes_passado = ws.find(mes_passado)
    col_mes_passado = cell_mes_passado.col

    # procura na planilha onde está a celula de Plano Juniakai
    cell_planojunia = ws.find(plano)
    row_planojunia = cell_planojunia.row

    # procura na planilha onde está a celula de Dívida
    cell_divida = ws.find("Dívida")
    row_divida = cell_divida.row

    # procura na planilha onde está a celula de "Lista dos pagantes"
    cell_lista_pagantes = ws.find("Lista dos pagantes")
    row_lista_pagantes = cell_lista_pagantes.row

    # popula a planilha de controle - qauntidade de planos de Junia
    ws.update_cell(row_planojunia,col_mes_passado,qtd_plano_juniakai)

    # popula a planilha de controle - quantidade de dinheiro devido naquele mês
    ws.update_cell(row_divida,col_mes_passado,divida_atual)

    # popula a planilha de controle - quem deveria ter pago naquele mês
    pula_linha = 0
    for i in ativos_df['Nome']:
        ws.update_cell(row_lista_pagantes+pula_linha,col_mes_passado,i)
        pula_linha +=1
    
    # chama função para receber o nome do mes passado
    mespassado_string = print_last_month()

    msg = f'Planilha de Divida com o Nipo preenchida - {mespassado_string}: R${divida_atual}'

    # Declaração dos parâmetros do Bot
    bot = {
        'webhook_url':'https://discord.com/api/webhooks/954242082288066580/jJVdVkn6A44yn_I5Dy7HI4xbJ0-atcZR645KJm5GyEw9qqrNkvNGsvLDdR-O4GGqre2n',
        'title_msg':f'DÍVIDA COM NIPO: {planilha} - {mespassado_string}',
        'msg':msg,
        'color':'0x2e702a',
        'name_author':f'Sr. Barriga - Planilha {planilha}',
        'author_icon':icon,
        'thumb':'',
        'footer':'Sr. Barriga'}
    # Chama a função para mandar a mensagem no bot
    discord_webhook(bot)

#preencher_divida('Departamento de Jovens','Juniakai','E4','Status','https://i.imgur.com/7XeLpEa.jpg',"","")
#preencher_divida('Tsubame 2022','TSUBAME','D2','Status Tsubame','https://i.imgur.com/aZbab9V.jpg','Cadastro Tsubame','Tsubame')
#preencher_divida('Tobu 2022','TOBU','D2','Status Tobu','https://i.imgur.com/ekgUNGx.jpg','Cadastro Tobu','Tobu')
#preencher_divida('ZENSHIN 2022','ZENSHIN','D2','Status Zenshin','https://i.imgur.com/nTGXzFm.gif','Cadastro Zenshin','Zenshin')