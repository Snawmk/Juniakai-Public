#!/bin/env python3
import gspread
import pandas as pd
from functions import get_google_sheet, discord_webhook, discord_webhook_table
from oauth2client.service_account import ServiceAccountCredentials
from discord_webhook import DiscordWebhook, DiscordEmbed
from operator import itemgetter

# Este script irá ler a planilha Departamento de Jovens e irá na aba de Cadastro
# Ele identifica as pessoas que estão faltando adicionar no grupo do Whatsapp,
# Bem como identifica pessoas que precisam tirar de algum grupo
# Envia Lista no What's app
# Executar 1 vez por mês

# define os nomes dos grupos do Junia
grupo_junia = "Juniakai Nipo Campinas 友.xlsx"
grupo_news = "[ NEWS ] JNC.xlsx"
grupo_shonen = "✨ [Shonen Junia-Kai]😁⚽🥁🏐🕺🏽.xlsx"
img_grupo_junia = "https://i.imgur.com/7XeLpEa.jpg"
img_grupo_news = "https://i.imgur.com/VYbOuXM.jpg"
img_grupo_shonen = "https://i.imgur.com/kYorMye.jpg"

# Conectar na planilha do Departamento de Jovens
records_data = get_google_sheet('Departamento de Jovens','Master Database')

# convert the json to dataframe
dados_df = pd.DataFrame.from_dict(records_data)

# filtrar planilha de presença para apenas pessoas ativas
ativos_df = dados_df.loc[dados_df['Status'] == 'ATIVO']
ativos_shonen_df = ativos_df.loc[ativos_df['Subs'] == 'Shonen']
ativos_coord_df = ativos_df.loc[ativos_df['Subs'] == 'Coord']

# cria lista de telefones que estão no cadastrodo Juniakai
lista_tel = list(ativos_df["Celular"])
lista_tel_shonen = list(ativos_shonen_df["Celular"])
lista_tel_coord = list(ativos_coord_df["Celular"])
lista_tel_all = list(dados_df["Celular"])

# função que normaliza os numeros de telefone na lista
def normaliza_tel(tel_list):
    tel_list = [str(x) for x in tel_list if x]
    tel_list_tratada = []
    for i in tel_list:
        a = i.replace("+","")
        a = a.replace("(","")
        a = a.replace(")","")
        a = a.replace("-","")
        a = a.replace(" ","")
        tel_list_tratada.append(a)
    return tel_list_tratada

#chama a função para criar listas de telefones
#lista_tel_tratada = somente ativos
lista_tel_tratada = normaliza_tel(lista_tel)
#lista_tel_tratada_shonen = somente shonens ativos
lista_tel_tratada_shonen = normaliza_tel(lista_tel_shonen)
#lista_tel_coord_tratada = somente os coordenadores
lista_tel_coord_tratada = normaliza_tel(lista_tel_coord)
#lista_tel_all_tratada = todos os cadastros
lista_tel_all_tratada = normaliza_tel(lista_tel_all)

# Cria uma lista das pessoas e numeros tratados dos junias ativos
nome_num_ativo = list(zip(ativos_df["Nome"],lista_tel_tratada))
nome_num_ativo_shonen = list(zip(ativos_shonen_df["Nome"],lista_tel_tratada_shonen))

# Define função para ler arquivo xlsx Excel
def read_file(name):
    data = pd.read_excel(name)
    return data

# Define a função para checkar se todos os membros que estão como ativos na planilha estão no grupo do Whatsapp
# A Função recebe um grupo de what'sapp e uma lista de nomes+numeros
def checkar_ativos(grupo,lista_ativos):
    # ler grupo do Whatsapp
    lista_junia = read_file(grupo)
    # define var apenas com a coluna "Phone Number" da planilha
    gp_junia_num = list(lista_junia["Phone Number \t\t\t\t\t"])

    # Transforma a lista gp_junia_num em string e corta o +55 do começo
    gp_junia_num = [str(x)[2:] for x in gp_junia_num if x]

    # Compara a lista de ativos da planilha com a lista de telefones no grupo do Juniakai
    lista_msg = []
    for i in lista_ativos:
        if i[1] in gp_junia_num:
            # Se estiver ativo, não faz nada
            pass
        else:
            # Se não estiver ativo, adiciona na lista lista_msg
            txt = f"\n- {i[0].strip()}: ({i[1]})"
            lista_msg.append(txt)

    # output do código em formato de mensagem do discord
    #msg = f"Junias ATIVOS no CADASTRO que não estão no grupo {grupo[:-5].upper()}: \n\n"
    msg = ""
    for i in range(len(lista_msg)):
        msg = msg + f"{lista_msg[i]} \n"

    # print da saida da msg do Discord para conferencia no terminal
    # print(msg)

    title = f"Junias ATIVOS no CADASTRO que não estão no grupo {grupo[:-5].upper()}: \n\n"

    return title, msg

# Define a função para checkar quem são os membros do grupo do Whatsapp 
# A Função recebe um grupo de what'sapp e uma lista de nomes+numeros
def checkar_grupo(grupo,lista_ativos,img):
    # ler grupo do Whatsapp
    lista_junia = read_file(grupo)
    # define var apenas com a coluna "Phone Number" da planilha
    gp_junia_num = list(lista_junia["Phone Number \t\t\t\t\t"])

    # Transforma a lista gp_junia_num em string e corta o +55 do começo
    gp_junia_num = [str(x)[2:] for x in gp_junia_num if x]

    # Cria uma pack com [0]Número do grupo whats, [1]Nome do perfil público do whats e [2]Nome do contato salvo no celular
    gp_junia_nome = list(zip(gp_junia_num,lista_junia["Contact's Public Display Name \t\t\t"],lista_junia["Saved Name \t\t\t\t\t"]))
    
    # aqui vamos extrair apenas os telefones dos ativos do cadastro
    nome_num_ativo2 = []
    for x in lista_ativos:
        nome_num_ativo2.append(x[1])

    # Compara a lista do WHATSAPP com a lista de ATIVOS no cadastro do Juniakai
    lista_msg = []
    for i in gp_junia_nome:
        if i[0] in nome_num_ativo2:
            # Se o telefone que estiver no grupo, estiver no cadastro como ativo
            # Não fazer nada...
            pass
        else:
            if i[0] not in lista_tel_all_tratada:
                # Se o telefone que estiver no grupo não estiver na lista de TODOS telefones cadastrados (não apenas dos ativos):
                txt = f"\n- {str(i[1]).strip()} | {str(i[2]).strip()}: {str(i[0])} | Não fez o cadastro!"
                lista_msg.append(txt)
            elif i[0] in lista_tel_coord_tratada:
                # Se o telefone for de um coordenador ativo, ignorar.
                pass
            else:
                # Então, o telefone foi encontrado no cadastro, mas a pessoa não está como ATIVO
                txt = f"\n- {str(i[1]).strip()} | {str(i[2]).strip()}: {str(i[0])} | Status Não-Ativo!"
                lista_msg.append(txt)

    # Re-ordena a lista pelo item na posição[1] = Nome
    lista_msg = sorted(lista_msg, key=itemgetter(1))

    # output do código em formato de mensagem do discord
    #msg = f"Junias que estão no grupo {grupo[:-5].upper()} e não estão ATIVOS no CADASTRO: \n\nNome Whats | Nome Contato : Telefone | Status \n\n"
    msg = ""
    for i in range(len(lista_msg)):
        msg = msg + f"{lista_msg[i]} \n"

    # print da saida da msg do Discord para conferencia no terminal
    # print(msg)

    title = f"Junias que estão no grupo {grupo[:-5].upper()} e não estão ATIVOS no CADASTRO: \n\n"

    title2, msg2 = checkar_ativos(grupo, lista_ativos)

    # Declaração dos parâmetros do Bot
    bot = {
        'webhook_url':'https://discord.com/api/webhooks/950961251574480986/Mvd2mEAAN13ie3gwsMBKBlXC6CetOyKwDEBwSnDuW6UWuGeq6FUu7yPdHj8CVYPlPWmw',
        'title_msg':f'Compara grupo {grupo[:-5].upper()} com junias ATIVOS no cadastro',
        'msg':"1) Compara quem está no grupo do Whatsapp e não está no cadastro como ATIVO e também 2) Compara quem está no cadastro como ATIVO que não está no grupo do Whatsapp",
        'color':'0x781912',
        'name_author':'Sr. Chekas - Planilha Departamento de Jovens',
        'author_icon':img,
        'Field1':"1) " + title,
        'txt_Field1':msg,
        'Field2':"2) " + title2,
        'txt_Field2':msg2,
        'thumb':'',
        'footer':'Sr. Chekas'}
    # Chama a função para mandar a mensagem no bot
    discord_webhook_table(bot)

# função para comparar os dois grupos fornecidos via .xlsx
def compara_grupos(grupo1,grupo2):

    def cria_pack(grupo):
        # ler grupo do Whatsapp
        lista_grupo = read_file(grupo)
        # define var apenas com a coluna "Phone Number" da planilha
        gp_nums = list(lista_grupo["Phone Number \t\t\t\t\t"])
        
        # Transforma a lista gp_junia_num em string e corta o +55 do começo
        gp_nums = [str(x)[2:] for x in gp_nums if x]

        # Cria uma pack com [0]Número do grupo whats, [1]Nome do perfil público do whats e [2]Nome do contato salvo no celular
        grupo1_pack = list(zip(gp_nums,lista_grupo["Contact's Public Display Name \t\t\t"],lista_grupo["Saved Name \t\t\t\t\t"]))
        return grupo1_pack

    gp1_pack = cria_pack(grupo1)
    gp2_pack = cria_pack(grupo2)

    # Cria listas dos telefones
    lista_tel_gp1 = []
    for i in gp1_pack:
        lista_tel_gp1.append(i[0])
    
        lista_tel_gp2 = []
    for i in gp2_pack:
        lista_tel_gp2.append(i[0])

    # É o comparas GRUPO 1 com GRUPO 2
    not_in_gp2 = []
    for i in gp1_pack:
        if i[0] not in lista_tel_gp2:
            txt = f"-> {i[1].strip()} | {i[2].strip()}: {i[0]}"
            not_in_gp2.append(txt)

    # É o comparas GRUPO 2 com GRUPO 1
    not_in_gp1 = []
    for i in gp2_pack:
        if i[0] not in lista_tel_gp1:
            txt = f"-> {i[1].strip()} | {i[2].strip()}: {i[0]}"
            not_in_gp1.append(txt)
    
    # Re-ordena as listas pelo item na posição[1] = Nome
    not_in_gp1 = sorted(not_in_gp1, key=itemgetter(1))
    not_in_gp2 = sorted(not_in_gp2, key=itemgetter(1))

    # output do código em formato de mensagem do discord
    msg = f"Comparei dois grupos de Whatsapp, e descobri quem falta adicionar em cada um, assim os dois grupos ficarão iguais!"
    msg1 = ""
    msg2 = ""
    for i in range(len(not_in_gp1)):
        msg1 = msg1 + f"{not_in_gp1[i]} \n"
    for i in range(len(not_in_gp2)):
        msg2 = msg2 + f"{not_in_gp2[i]} \n"

    # Coloca um valor "-" caso não tenha ngm nas listas, se a variável estiver vazia dá pau no WebHook do Discord
    if msg1 == "":
        msg1 = "OK: Não falta adicionar ninguem"
    if msg2 == "":
        msg2 = "OK: Não falta adicionar ninguem"

    # print da saida da msg do Discord para conferencia no terminal
    # print(f"Pessoas que não estão no {grupo1[:-5].upper()}: \n {msg1}")
    # print(f"Pessoas que não estão no {grupo2[:-5].upper()}: \n {msg2}")

    # Declaração dos parâmetros do Bot
    bot = {
        'webhook_url':'https://discord.com/api/webhooks/950961251574480986/Mvd2mEAAN13ie3gwsMBKBlXC6CetOyKwDEBwSnDuW6UWuGeq6FUu7yPdHj8CVYPlPWmw',
        'title_msg':f'GRUPOS DIFF: {grupo1[:-5].upper()} vs {grupo2[:-5].upper()}',
        'msg':msg,
        'color':'0xba8e14',
        'name_author':'Sr. Chekas - Planilha Departamento de Jovens',
        'author_icon':'https://static.abcteach.com/free_preview/m/mathsymbolnotequalrgb_p.png',
        'Field1':f'Not in {grupo1[:-5].upper()}:',
        'txt_Field1':msg1,
        'Field2':f'Not in {grupo2[:-5].upper()}:',
        'txt_Field2':msg2,
        'thumb':'',
        'footer':'Sr. Chekas'}
    # Chama a função para mandar a mensagem no bot
    discord_webhook_table(bot)

# Executa as funções
#checkar_grupo(grupo_junia,nome_num_ativo,img_grupo_junia)
#checkar_grupo(grupo_news,nome_num_ativo,img_grupo_news)
#checkar_grupo(grupo_shonen,nome_num_ativo_shonen,img_grupo_shonen)
#compara_grupos(grupo_junia,grupo_news)

