import pandas as pd
from functions import get_google_sheet, discord_webhook, get_days_until_birthday
from datetime import datetime
from operator import itemgetter

# Este script irá ler a planilha Departamento de Jovens e irá na aba de de cadastro
# Ele identifica as pessoas que farão aniversário dentro dos prox 15 dias
# E envia uma mensagem no grupo do Discord
# Executar a cada 15 dias

# Define a data atual
data_atual = datetime.today().date()
data_em_texto = data_atual.strftime("%d/%m/%Y")

# Conectar na planilha do Departamento de Jovens
records_data = get_google_sheet('Departamento de Jovens','Master Database')

# convert the json to dataframe
cadastro_df = pd.DataFrame.from_dict(records_data)

# filtrar planilha de presença para apenas pessoas ativas
cadastro_df = cadastro_df.loc[cadastro_df['Status'] == 'ATIVO']

# Define a lista de datas de nascimento
lista_nasc = cadastro_df["Nascimento"]
lista_nasc = [x for x in lista_nasc if x]
lista_nasc_tratada = []
for i in lista_nasc:
    count = len(i)
    if count == 10:
        data = i[:6] +  i[8:]
        #print(i)
        #print(len(i))
        #print(data)
        lista_nasc_tratada.append(data)
    elif count == 9:
        data = i[:5] +  i[7:]
        lista_nasc_tratada.append(data)
    else:
        lista_nasc_tratada.append(i)

# Define lista com nomes do pessoal
nome_data = list(cadastro_df["Nome"])
nome_data = [x for x in nome_data if x]

# Define lista com idade do pessoal 
idade = list(cadastro_df["Idade"])

# Transforma dados em formato date
lista_bdays = []
for i in lista_nasc_tratada:
    linha = datetime.strptime(i,"%d/%m/%y").date()
    bday_days = get_days_until_birthday(linha,data_atual)
    lista_bdays.append(bday_days)

if (len(nome_data)== len(lista_nasc_tratada)):
    lista = list(zip(nome_data,lista_bdays,lista_nasc_tratada,idade))

    niver_prox = []
    for i in lista:
        if (i[1] <= 15):
            niver_prox.append(i)

    niver_prox = sorted(niver_prox, key=itemgetter(1))

    #output do código em formato de mensagem do discord
    msg = "Lista das pessoas farão aniversário nos próximos 15 dias: \n\n"
    for i in range(len(niver_prox)):
        msg = msg + f"{niver_prox[i][2][:5]}: {niver_prox[i][0]} ({niver_prox[i][3]+1} anos) - Faltam {niver_prox[i][1]} dias\n"
    #print(msg)
else:
    msg = "Erro! Provavelmente está faltando alguma data de aniversário no cadastro de ATIVOS! Favor verificar."

# Declaração dos parâmetros do Bot
bot = {
    'webhook_url':'https://discord.com/api/webhooks/950218541389451274/PCAH0RZwDN3cIvqBDUVBEoZhNbMmMIG_XcimPUdBKlkkz8ZoMgil_TOoV1kzD_4GlpQx',
    'title_msg':'Próximos aniversariantes',
    'msg':msg,
    'color':'0x000080',
    'name_author':'Sr. Aniversários - Planilha Departamento de Jovens',
    'author_icon':'https://i.imgur.com/nm1xX16.png',
    'thumb':'',
    'footer':'Sr. Aniversários'}
# Chama a função para mandar a mensagem no bot
discord_webhook(bot)

