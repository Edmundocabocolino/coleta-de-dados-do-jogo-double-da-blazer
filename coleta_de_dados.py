import sqlite3
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


def criar_tabela():
    # Conecta ao banco de dados SQLite (cria o banco se não existir)
    conexao = sqlite3.connect('../atualizacao.db')
    cursor = conexao.cursor()

    # Cria uma tabela para armazenar os dados
    cursor.execute('''CREATE TABLE IF NOT EXISTS dados (
                        id INTEGER PRIMARY KEY,
                        conteudo TEXT
                    )''')

    # Salva as alterações e fecha a conexão
    conexao.commit()
    conexao.close()


def inserir_dados(conteudo):
    # Conecta ao banco de dados SQLite
    conexao = sqlite3.connect('../atualizacao.db')
    cursor = conexao.cursor()

    # Insere os dados na tabela
    cursor.execute('''INSERT INTO dados (conteudo) VALUES (?)''', (conteudo,))

    # Salva as alterações e fecha a conexão
    conexao.commit()
    conexao.close()


def coletar_dados():
    # Inicializa o driver do Firefox
    options = webdriver.FirefoxOptions()
    options.headless = True  # Para rodar em modo headless (sem interface gráfica)
    driver = webdriver.Firefox(options=options)

    # URL base do site que você quer raspar
    base_url = 'https://blaze1.space/pt/games/double?modal=double_history_index'
    driver.get(base_url)

    try:
        while True:
            try:
                # Aguarda até que o elemento de histórico seja visível na página
                elemento_historico = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'history__double'))
                )

                # Coleta os dados da página atual do histórico
                dados = elemento_historico.text
                inserir_dados(dados)

                # Filtra os dados e verifica se a condição foi concretizada
                verificar_condicao(dados)

                # Aguarda 15 segundos antes de atualizar novamente
                time.sleep(15)

                # Navega para a URL novamente para obter os novos dados
                driver.refresh()

            except TimeoutException:
                print("TimeoutException: Elemento de histórico não encontrado.")
                break

    except TimeoutException:
        print("TimeoutException: Elemento de histórico não encontrado.")

    # Fecha o navegador
    driver.quit()

import tkinter as tk


def exibir_aviso(mensagem):
    # Função para exibir um pop-up com a mensagem de aviso
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal

    # Exibe a mensagem de aviso em uma janela pop-up
    tk.messagebox.showwarning("Aviso", mensagem)

def verificar_condicao(dados):
    def verificar_condicao(dados):
        # Função para verificar a condição e exibir um aviso se necessário
        dados_filtrados = filtrar_dados(dados)
        numeros_nao_zero = len(dados_filtrados)

        if numeros_nao_zero > 10:
            # Se o número de números não zero consecutivos for maior que 50, exibe um aviso
            mensagem = "AVISO: O número de números não zero consecutivos é maior que 10!"
            exibir_aviso(mensagem)

    def main():
        criar_tabela()
        coletar_dados()

    if __name__ == "__main__":
        main()

def filtrar_dados(dados):
    # Expressão regular para encontrar os números na string
    regex = r'\b\d+\b'
    # Aplica a expressão regular para extrair os números
    numeros = re.findall(regex, dados)

    # Se não houver números encontrados, retorna 0
    if not numeros:
        print("Não foram encontrados números no texto.")
        return 0

    # Inicializa uma variável para armazenar o número de números não zero consecutivos
    contador_numeros = 0

    # Itera sobre os números encontrados
    for numero in numeros:
        numero = int(numero)
        if numero != 0:
            # Incrementa o contador de números não zero
            contador_numeros += 1
        else:
            # Quando encontrar um zero, imprime a contagem de números não zero consecutivos
            if contador_numeros > 0:
                print(f"Sairam {contador_numeros} números antes do zero.")
            # Reinicia a contagem
            contador_numeros = 0

    # Se a contagem não foi reiniciada antes do final, imprime a contagem
    if contador_numeros > 0:
        print(f"Sairam {contador_numeros} números antes do zero.")



def encontrar_intervalo_maximo(dados_filtrados):
    # Inicializa variáveis para armazenar os intervalos entre os zeros
    intervalo_atual = 0
    intervalo_maximo = 0

    # Itera sobre os dados filtrados
    for dado in dados_filtrados:
        if dado == '0':
            if intervalo_atual > intervalo_maximo:
                intervalo_maximo = intervalo_atual
            intervalo_atual = 0
        else:
            intervalo_atual += 1

    return intervalo_maximo

def filtrar_e_contar(dados):
    # Dividir os dados em linhas
    linhas = dados.split('\n')

    # Inicializar variável para armazenar os resultados
    resultados = []

    # Inicializar contador de números não zero consecutivos
    contador_numeros = 0

    # Iterar sobre as linhas
    for linha in linhas:
        # Tentar converter a linha para um número inteiro
        try:
            numero = int(linha)
            # Se o número for zero, adicionar o resultado à lista de resultados
            if numero == 0:
                resultados.append(f"Sairam {contador_numeros} números antes do zero.")
                contador_numeros = 0
            else:
                # Incrementar o contador de números não zero consecutivos
                contador_numeros += 1
        # Se a linha não puder ser convertida para um número, ignorá-la
        except ValueError:
            continue

    # Se houver números não zero consecutivos no final dos dados, adicionar o resultado à lista de resultados
    if contador_numeros > 0:
        resultados.append(f"Sairam {contador_numeros} números antes do zero.")

    # Salvar o resultado em um arquivo de texto
    with open("resultado.txt", "w") as arquivo:
        for resultado in resultados:
            arquivo.write(resultado + "\n")

    # Imprimir os resultados em uma única linha
    #print(' - '.join(resultados))


def verificar_condicao(dados):
    filtrar_e_contar(dados)

def main():
    criar_tabela()
    coletar_dados()


if __name__ == "__main__":
    main()
