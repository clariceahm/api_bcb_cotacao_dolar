###------------------------------------------------------------------------------------------------
## Description: Controls the data extraction routine, loading data into the SQLServer database and sending information by email
###------------------------------------------------------------------------------------------------


##------------------------
## REQUIRED PACKAGES
##------------------------
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import extract_api
import connect_bd
import send_email


##------------
## TODAY
##------------
hoje = datetime.now()
ontem = hoje - timedelta(days=1)

# Getting the day of the week (0=Monday, 6=Sunday)
dia_semana = ontem.weekday()

ontem = ontem.strftime('%m-%d-%Y')
ontem = "'" + ontem + "'"

## Name of database table with dollar rate
table_name = 'Cotacao_Dolar_BCB_TESTE'


##------------
## URL
##------------
api_bc = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao="
url = api_bc + ontem + "&$top=100&$format=json&$select=cotacaoCompra,cotacaoVenda,dataHoraCotacao"


##------------
## EXTRACT DOLLAR RATE
##------------

try:
    df = extract_api.dollar_rate(url)

    # Use json_normalize to transform the list of nested dictionaries into DataFrame
    df = pd.json_normalize(
        df,
        sep='_',  # Separator for nested columns
        max_level=1  # Maximum nesting level to consider
    )

    df.rename(columns = {'cotacaoCompra':'cotacao_compra','cotacaoVenda':'cotacao_venda','dataHoraCotacao':'data_cotacao'},inplace = True)
    df.loc[:,'data_carga'] = hoje
    ## Changing data type
    df['cotacao_compra'] = df['cotacao_compra'].astype('float64')
    df['cotacao_venda'] = df['cotacao_venda'].astype('float64')
    df['data_cotacao'] = pd.to_datetime(df['data_cotacao'])
    df['data_carga'] = pd.to_datetime(df['data_carga'])

    # Getting the day of the week (0=Monday, 6=Sunday)
    df.loc[:,'dia_semana'] = df['data_cotacao'].dt.weekday
    conditionlist = [
        (df['dia_semana'] == 0),
        (df['dia_semana'] == 1),
        (df['dia_semana'] == 2),
        (df['dia_semana'] == 3),
        (df['dia_semana'] == 4),
        (df['dia_semana'] == 5)]
    choicelist = ['segunda-feira', 'terca-feira', 'quarta-feira','quinta-feira','sexta-feira','sabado']
    df['dia_semana'] = np.select(conditionlist, choicelist, default='domingo')
       
    df = df[['cotacao_compra','cotacao_venda','data_cotacao','dia_semana','data_carga']]
except:
    print('The api returned no value for the date ',ontem)
    query = '''  SELECT * FROM ''' + table_name + ''' WHERE data_cotacao = (SELECT MAX(data_cotacao) FROM ''' + table_name + ''');'''

    df = connect_bd.query_bd(query)
    df.loc[0,'data_cotacao'] = ontem
    df.loc[0,'dia_semana'] = dia_semana
    conditionlist = [
        (df['dia_semana'] == 0),
        (df['dia_semana'] == 1),
        (df['dia_semana'] == 2),
        (df['dia_semana'] == 3),
        (df['dia_semana'] == 4),
        (df['dia_semana'] == 5)]
    choicelist = ['segunda-feira', 'terca-feira', 'quarta-feira','quinta-feira','sexta-feira','sabado']
    df['dia_semana'] = np.select(conditionlist, choicelist, default='domingo')
    df.loc[0,'data_carga'] = hoje


##--------------------
## SAVING DATA IN DATABASE
##--------------------

## INSERT
connect_bd.insert(table_name, df)


##-----------------------
## SENDING EMAIL
##-----------------------
send_email.sending_email(df)
