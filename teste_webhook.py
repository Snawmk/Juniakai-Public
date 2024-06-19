#!/bin/env python3
from functions import webhook, entrar_planilha, get_google_sheet, discord_webhook
import pandas as pd
import numpy as np

botpress_url = 'https://webhook.botpress.cloud/a0c82534-43ee-4914-b6e4-cfba77d170d3'

dados = {
    'Nome':'Pedro Takeshi Odo Lopes',
    'Data_de_Nascimento': '07/11/1998',
    'Mensalidade': 'R$ 10,00',
    'Divida': 'R$ 150,00'
}



# Conectar na planilha do Departamento de Jovens
records_data = get_google_sheet(planilha,'Presença')

# convert the json to dataframe
presenca_df = pd.DataFrame.from_dict(records_data)

# filtrar planilha de presença para apenas pessoas ativas
ativos_df = presenca_df.loc[presenca_df['Status'] == 'ATIVO']

webhook(botpress_url,dados)