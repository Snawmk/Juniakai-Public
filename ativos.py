#!/bin/env python3
import pandas as pd
from functions import discord_webhook_table, get_google_sheet


def verifica_ativo_novatos(planilha,img):

  # Este script irá ler a planilha Departamento de Jovens e irá na aba de presença.
  # Ele identifica as pessoas que estão faltando além do limite para defini-lo como ativo
  # E envia uma mensagem no grupo do Discord
  # Executar 1 vez por mês

  #limite de domingos consecutivos para ser considerado inativo
  limite_inativo = 8

  #lista de pessoas para inativar
  lista_inativar = []

  # Conectar na planilha do Departamento de Jovens
  records_data = get_google_sheet(planilha,'Presença')

  # convert the json to dataframe
  presenca_df = pd.DataFrame.from_dict(records_data)

  # filtrar planilha de presença para apenas pessoas ativas
  ativos_df = presenca_df.loc[presenca_df['Status'] == 'ATIVO']

  # filtrar apenas 'p's e 'f's do df de ativos
  presenca_ativos_df = ativos_df.drop(columns=['Apelido', 'Status'])

  # criar lista com as informações
  lista_presenca = []
  for index, row in presenca_ativos_df.iterrows():
      rows = list(row.values)
      # Remove blank values from the list
      rows = [x for x in rows if x]
      lista_presenca.append(rows)

  # loop para avaliar cada entrada da lista de presença
  for pessoa in lista_presenca:
    # contador de faltas de cada pessoa
    contf = 0
    # lista temporaria para ser revertida
    list_temp = pessoa
    list_temp.reverse()
    # lista que irá receber os valores em minúsculo
    list_temp2 = []
    
    # for que irá forçar as entradas da planilha em minúsculo
    for minusculo in list_temp:
      try:
        list_temp2.append(minusculo.lower())
      finally:
        continue

    # for que irá contar a quantidade de faltas por pessoa
    for pf in list_temp2:
      if pf == "f":
        contf += 1
        if contf >= limite_inativo:
          posicao_nome = (len(pessoa) - 1) -1
          lista_inativar.append((pessoa[posicao_nome].strip() + " - " + str((contf))))
          if len(lista_inativar)>=2 and lista_inativar[-2] == pessoa[posicao_nome].strip() + " - " + str((contf-1)):
            lista_inativar.pop(-2)
      elif pf == "p":
        break
      elif pf == "-":
        pass

  #print(lista_inativar)
  lista_inativar = str(lista_inativar)
  lista_inativar = lista_inativar.replace("'", "")
  lista_inativar = lista_inativar.replace("[", "")
  lista_inativar = lista_inativar.replace("]", "")
  lista_inativar = lista_inativar.replace(",", "\n")
  if (lista_inativar == ""):
    lista_inativar = "Ninguém"

  #output do código em formato de mensagem do discord
  msg1 = (f"\n \n{lista_inativar}")

  #verifica os novatos que devem ser chamados para conversar
  #limite de domingos consecutivos para ser considerado chamar o novato e perguntar se vai continuar no junia
  limite_novato = 6

  #lista de pessoas para inativar
  lista_novatos = []

  # filtrar planilha de presença para apenas pessoas ativas
  novatos_df = presenca_df.loc[presenca_df['Status'] == 'NOVATO']

  # filtrar apenas 'p's e 'f's do df de ativos
  presenca_novatos_df = novatos_df.drop(columns=['Apelido', 'Status'])

  # criar lista com as informações
  lista_presenca_novatos = []
  for index, row in presenca_novatos_df.iterrows():
      rows = list(row.values)
      # Remove blank values from the list
      rows = [x for x in rows if x]
      lista_presenca_novatos.append(rows)

  # loop para avaliar cada entrada da lista de presença
  for pessoa in lista_presenca_novatos:
    # contador de presença/faltas de cada novato
    contf = 0
    # lista temporaria para ser revertida
    list_temp = pessoa
    list_temp.reverse()
    # lista que irá receber os valores em minúsculo
    list_temp3 = []
    
    # for que irá forçar as entradas da planilha em minúsculo
    for minusculo in list_temp:
      try:
        list_temp3.append(minusculo.lower())
      finally:
        continue

    # for que irá contar a quantidade de faltas por pessoa
    for pf in list_temp3:
      if (pf == "f") or (pf == "p"):
        contf += 1
        if contf >= limite_novato:
          posicao_nome = (len(pessoa) - 1) -1
          lista_novatos.append(pessoa[posicao_nome].strip())
          break
      elif pf == "-":
        pass

  lista_novatos = str(lista_novatos)
  lista_novatos = lista_novatos.replace("'", "")
  lista_novatos = lista_novatos.replace("[", "")
  lista_novatos = lista_novatos.replace("]", "")
  lista_novatos = lista_novatos.replace(",", "\n")
  if (lista_novatos == ""):
    lista_novatos = "Ninguém :)"

  #output do código em formato de mensagem do discord
  msg2 = (f"\n \n{lista_novatos}")

  # Declaração dos parâmetros do Bot
  bot = {
      'webhook_url':'secret',
      'title_msg':f'Verificação semanal de ATIVOS e NOVATOS - {planilha}',
      'msg':'',
      'Field1':f'Lista dos ATIVOS ques estão faltando há mais de {int((limite_inativo/4))} meses: \n',
      'txt_Field1':f'{msg1}',
      'Field2':f'Lista dos NOVATOS que passaram de um mês (tempo experimental): \n',
      'txt_Field2':f'{msg2}',
      'color':'0xff0000',
      'name_author':f'Sr. X9 - Planilha {planilha}',
      'author_icon':'https://i.imgur.com/dhPhkQt.png',
      'thumb':img,
      'footer':'Sr. X9'}
  # Chama a função para mandar a mensagem no bot
  discord_webhook_table(bot)

verifica_ativo_novatos('Departamento de Jovens','https://i.imgur.com/7XeLpEa.jpg')
#verifica_ativo_novatos('Tsubame 2022','https://i.imgur.com/aZbab9V.jpg')
#verifica_ativo_novatos('Tobu 2022','https://i.imgur.com/ekgUNGx.jpg')
