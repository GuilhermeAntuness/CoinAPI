import requests
import json
import os
from dotenv import load_dotenv
import time

load_dotenv()

api_key = os.getenv("KEY")


def buscar_moedas():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

    headers = {
        'Accept': 'application/json',
        'X-CMC_PRO_API_KEY' : api_key
    }

    params = {
        "start": "1",         # início da listagem
        "limit": "10",        # quantas moedas listar
        "convert": "BRL",     # moeda de conversão
    }

    response = requests.get(url, headers=headers, params=params)
    print(response.status_code)

    if response.status_code == 200:
        data = response.json()
        for coin in data["data"]:
            print(f"{coin['name']} ({coin['symbol']}): R${coin['quote']['BRL']['price']:.2f}")


def buscar_moeda_por_symbol(symbol):

    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

    headers = {
        'Accept': 'application/json',
        'X-CMC_PRO_API_KEY' : api_key
    }

    params = {
                # início da listagem
        "symbol" : symbol,        # quantas moedas listar
        "convert": "BRL",     # moeda de conversão

    }

    try:

        response = requests.get(url, headers=headers, params=params)
        print(response.status_code)

        if response.status_code == 200:
            data = response.json()
            return data
        
    except requests.exceptions.RequestException as e:
        print('Erro de requisição', e)
        return None
        
        
def buscar_moeda_por_nome(name):

    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

    headers = {
        'Accept': 'application/json',
        'X-CMC_PRO_API_KEY' : api_key
    }

    params = {
                # início da listagem
        "slug" : name,        # quantas moedas listar
        "convert": "BRL",     # moeda de conversão

    }
    
    try:

        response = requests.get(url, headers=headers, params=params)
        print(response.status_code)

        if response.status_code == 200:
            data = response.json()
            return data
        
    except requests.exceptions.RequestException as e:
        print('Erro de requisição', e)
        return None
        

def mostra_moeda():

    moeda = input('Digite o nome ou symbolo da moeda que deseja ver: ')
    print('-~'*25)

    if len(moeda) == 3:
        data = buscar_moeda_por_symbol(moeda.upper())

    else: 
        data = buscar_moeda_por_nome(moeda)


    if data:
        for symbol in data["data"]:
            coin = data['data'][symbol]["symbol"]
            name = data['data'][symbol]["name"]
            price = data['data'][symbol]["quote"]['BRL']["price"]

            print('Nome | CODE    | Preço')
            print (f"{name}  | {coin} | R$: {price:.2f}")
            print('-~'*25)
        
        favorita = input('Adicionar como favorita? [S/N]: ')

        if favorita in 'sS':
            for i in favoritas:
                if not name in favoritas['name']:
                    print(f'{name} Já está na lista de favoritos')

            else:
                favoritas.append({'coin':coin, 'name': name, 'price': price})
                print(f'{name} Adicionado a lista de favoritos')
                time.sleep(1)
        
        historico.append(name)
    
    else:
        print(f' "{moeda}" Não encontrado')


def menu():
    print('-='*25)
    print('0 - Sair\n' \
          '1 - Buscar preço de uma moeda\n' \
          '2 - Ver moedas favoritas\n' \
          '3 - Ver histórico de consultas'
            )
    print()
    opcao = input('Digite a opção que você deseja: ')
    print('-='*25)
    return opcao
    
         


if __name__ == "__main__":

    favoritas = []
    historico = []

    try:
        while True:
            opcao = menu()

            if opcao == '0':
                print('Saindo...')
                time.sleep(1)
                exit()
            
            elif opcao == '1':
                mostra_moeda()
            
            elif opcao == '2':
                for i in favoritas:
                    print (f"{i['name']}  | {i['coin']} | R$: {i['price']:.2f}")

            elif opcao == '3':
                for i in historico:
                    print(i)
            
            else:
                print('Opção invalida')
                continue

    except KeyboardInterrupt:
        print('\nPrograma finalizado pelo usuário')
        exit()






   