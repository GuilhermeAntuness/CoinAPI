import requests
import json
import os
from dotenv import load_dotenv
import time
from collections import Counter

load_dotenv()

api_key = os.getenv("KEY")


def get_headers():
    return {
        'Accept': 'application/json',
        'X-CMC_PRO_API_KEY': api_key
    }

def get_top_cryptos(quantity):
    """
    Retorna uma lista com as principais criptomoedas em ordem de valor de mercado.

    Args:
        quantity (int): Quantidade de criptomoedas a serem retornadas.

    Returns:
        dict: Dados das criptomoedas retornados pela API.
    """
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

    headers = get_headers()

    params = {
        "start": "1",
        "limit": quantity,
        "convert": "BRL",
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()


def get_crypto_by_symbol(symbol):
    """
    Retorna os dados de uma criptomoeda específica com base no símbolo.

    Args:
        symbol (str): Símbolo da criptomoeda (ex: BTC, ETH).

    Returns:
        dict or None: Dados da criptomoeda ou None em caso de erro.
    """
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

    headers = get_headers()

    params = {
        "symbol": symbol,
        "convert": "BRL",
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print('Erro de requisição:', e)
        return None


def get_crypto_by_name(slug_name):
    """
    Retorna os dados de uma criptomoeda específica com base no nome (slug).

    Args:
        slug_name (str): Nome da criptomoeda no formato slug (ex: bitcoin, ethereum).

    Returns:
        dict or None: Dados da criptomoeda ou None em caso de erro.
    """
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

    headers = get_headers()

    params = {
        "slug": slug_name,
        "convert": "BRL",
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException as e:
        print('Erro de requisição:', e)
        return None


def show_crypto():
    """
    Solicita uma criptomoeda ao usuário e exibe seus dados.
    Adiciona ao histórico e permite marcar como favorita.
    """
    crypto = input('Digite o nome ou símbolo da moeda que deseja ver: ').strip()
    print('-~' * 25)

    try:

        if len(crypto) <= 5:
            data = get_crypto_by_symbol(crypto.upper())
        else:
            data = get_crypto_by_name(crypto)

        if data["data"]:

            for symbol in data["data"]:
                coin = data['data'][symbol]["symbol"]
                name = data['data'][symbol]["name"]
                price = data['data'][symbol]["quote"]['BRL']["price"]
            
            if not price:
                price = 0.00

            # ---------------------------------------------------------------
            # Exibição formatada da tabela com colunas alinhadas:
            # - Utiliza largura fixa para garantir que todos os dados fiquem
            #   bem posicionados, mesmo com nomes ou valores diferentes.
            # - {:<15} → alinha o texto à ESQUERDA ocupando até 15 caracteres
            # - {:<6}  → alinha o texto à ESQUERDA ocupando até 6 caracteres
            # - {:>12,.2f} → alinha à DIREITA, com separador de milhar (,)
            #   e 2 casas decimais (.2f), ideal para exibir valores monetários
            # - A separação com "|" facilita a leitura da tabela no terminal.
            # ---------------------------------------------------------------

            print("-" * 50)
            print(f"{'Nome':<15} | {'CODE':<6} | {'Preço':>15}")
            print("-" * 50)
            print(f"{name:<15} | {coin:<6} | R$: {float(price):>12,.2f}")
            print("-" * 50)

            add_favorite = input('Adicionar como favorita? [S/N]: ')

            # ---------------------------------------------------------------
            # Verifica se a moeda já está na lista de favoritas antes de adicionar:
            # - Usa 'any()' para percorrer a lista 'favoritas' e verificar se já
            #   existe um item com o mesmo 'coin'.
            # - Se nenhum item na lista tiver o mesmo símbolo, o novo dicionário
            #   {'coin': coin, 'name': name, 'price': price} será adicionado.
            # - Isso evita duplicatas na lista com base no campo 'coin'.
            # ---------------------------------------------------------------
            if add_favorite in 'sS':
                if not any(fav['coin'] == coin for fav in favorites):
                    favorites.append({'coin': coin, 'name': name, 'price': price})
                else:
                    print()
                    print(f'A moeda {coin} já está na sua lista de favoritos!')

            history.append(name)
        else:
            print(f'"{crypto}" não encontrado.')

    except TypeError:
        print('A moeda solicitada não foi encontrada')


def menu():
    """
    Exibe o menu principal do programa e solicita a escolha do usuário.

    Returns:
        str: Opção digitada pelo usuário.
    """
    print('-=' * 25)
    print()
    print(' MENU '.center(50, '-'))
    print()
    print('0 - Sair\n' \
          '1 - Buscar preço de uma moeda\n' \
          '2 - Ver moedas favoritas\n' \
          '3 - Ver principais moedas\n' \
          '4 - Ver histórico de consultas')
    print()
    option = input('Digite a opção que você deseja: ')
    print('-=' * 25)
    return option


if __name__ == "__main__":

    favorites = []
    history = []

    try:
        while True:
            option = menu()

            if option == '0':
                print('Saindo...')
                time.sleep(1)
                break

            elif option == '1':
                show_crypto()

            elif option == '2':
                print(f" Lista de Favoritas ".center(50, '~'))
                for fav in favorites:
                    print(f"{fav['name']:<15}  | {fav['coin']:<6} | R$: {fav['price']:<12.2f}")

            elif option == '3':
                
                while True:
                    try:
                        count = int(input('Quantas moedas você quer ver? '))
                    except ValueError:
                        print('Valor invalido')
                    else:
                        break

                data = get_top_cryptos(count)

                print()
                print(f' Principais Moedas '.center(50, '~'))

                for coin in data["data"]:
                    print(f"{coin['name']:<15} | ({coin['symbol']:^6}) | R${coin['quote']['BRL']['price']:<16,.2f}")

            elif option == '4':
                if not history:
                    print(' Histórico vazio '.center(50, '~'))
                    continue

                c = Counter(history)
                for k, v in c.items():
                    if v < 2:
                        print(f'{k} - {v} vez')
                    else:
                        print(f'{k} - {v} vezes')


            else:
                print('Opção inválida')
                continue

    except KeyboardInterrupt:
        print('\nPrograma finalizado pelo usuário')
        exit()
    
    except ValueError as e:
        print('Valor invalido!', e)
        







   