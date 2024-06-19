#!/bin/env python3
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from functions import get_google_sheet, entrar_planilha


# Este código irá verificar quais pessoas não tem carteirinha de mensalidade localizada no Google Drive do Juniakai, fará uma Cópia do modelo e atribuirá as pessoas que ainda não tem carteirinha.

# Nome da planilha utilizada como MODELO da Carteirinha Digital
modelo = '1QC4pSC4vVx1ZDpQ0MjmVBgZHtqK4qT--H1reZ_PH9FE'
folder_id_destino = '1CmhlOR1IjMsy8deQdc02QQhOkz6kz4GP'

# Entra na planilha para poder escrever em algumas células mais pra frente
sheet = entrar_planilha('Projeto Carteirinha', 'Controle')

def copia_modelo(planilha_modelo, nome_planilha_destino, folder_id):
    # define the scope
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name("juniakai-7c58c121939a.json", scope)
    #creds = ServiceAccountCredentials.from_json_keyfile_dict(my_secret, scope)

    # authorize the clientsheet 
    client = gspread.authorize(creds)

    # copy the spreadsheet
    client.copy(planilha_modelo, title=nome_planilha_destino, copy_permissions=True, folder_id=folder_id)


# Conectar na planilha do Departamento de Jovens e Projeto Carteirinha
records_data = get_google_sheet('Departamento de Jovens','Master Database')
records_data2 = get_google_sheet('Projeto Carteirinha','Controle')

# convert the json to dataframe
database_df = pd.DataFrame.from_dict(records_data)
carteirinha_df = pd.DataFrame.from_dict(records_data2)

# filtrar planilha de presença para apenas pessoas ativas
ativos_df = database_df.loc[database_df['Status'] == 'ATIVO']

# lista nomes ATIVOS
lista_ativos = list(ativos_df["Nome"])

# lista pessoas que já tem carteirinha
lista_carteirinha = list(carteirinha_df['Pessoa'])

# lista de pessoas ativas para adicionar no controle de carteirinhas
lista_add = []

# lista de pessas que que serão marcadas como inativas
lista_inativos = []

# ID da planilha nova que será criada. Essa variável será utilizada para compor o endereço URL de acesso à planilha
sheet_id = ""

# lista de pessoas que estão no controle de carteirinhas mas que não estão mais ativas
for inativos in lista_carteirinha:
    if inativos in lista_ativos:
        continue
    else:
        lista_inativos.append(inativos)
        # Escreve na planilha que o individuo é Inativo
        sheet.update_cell(sheet.find(inativos).row,1,"Inativo")

# Compara os nomes dos ativos com os nomes que já tem carteirinha
for ativos in lista_ativos:
    if ativos in lista_carteirinha:
        continue
    else:
        lista_add.append(ativos)
        # Escreve na planilha que o individuo é ATIVO
        row = len(lista_carteirinha)+2
        sheet.update_cell(row,1,"ATIVO")
        sheet.update_cell(row,2,ativos)
        # Executa a função de criar uma planilha nova
        copia_modelo(modelo,ativos,folder_id_destino)
        # Escreve o nome na celula chave Row 3,Col 1 na nova planilha que foi criada com o nome do inidivio 
        sheet_destino = entrar_planilha(ativos, 'JUNIAKAI')
        sheet_destino.update_cell(3,1,ativos)
        # Escreve na planilha de Controle a URL da planilha nova
        sheet.update_cell(row,3,sheet_destino.url)


