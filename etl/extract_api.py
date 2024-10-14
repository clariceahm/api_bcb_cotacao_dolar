###------------------------------------------------------------------------------------------------
## Description: Extract the dollar rate in the central bank's API
###------------------------------------------------------------------------------------------------

##------------------------
## REQUIRED PACKAGES
##------------------------

## To access the central bank API
import requests
import json


def dollar_rate(url):
    res = requests.get(url, timeout=None)
    if res.status_code == 200:
        rate = json.loads(res.content)
        ## Removing unnecessary items from the dictionary
        rate.pop('@odata.context')
        print(rate)
        values = rate['value']
    else:
        print('Not found: ')
        values = {
                    'cotacaoCompra': '',
                    'cotacaoVenda': '',
                    'dataHoraCotacao': ''
                    }

    return(values)