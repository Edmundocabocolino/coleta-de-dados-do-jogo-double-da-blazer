# -*- coding: utf-8 -*-
import sqlite3
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

def criar_tabela():
    conexao = sqlite3.connect('../atualizacao1.db')
    cursor = conexao.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS dados (
                        id INTEGER PRIMARY KEY,
                        conteudo TEXT
                    )''')
    conexao.commit()
    conexao.close()

def inserir_dados(conteudo):
    conexao = sqlite3.connect('../atualizacao1.db')
    cursor = conexao.cursor()
    cursor.execute('''INSERT INTO dados (conteudo) VALUES (?)''', (conteudo,))
    conexao.commit()
    conexao.close()

def coletar_dados(driver):
    try:
        driver.refresh()  # Atualizar a página antes de coletar os dados
        elemento_historico = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, 'history__double'))
        )
        dados = elemento_historico.text
        inserir_dados(dados)
        verificar_condicao(dados)
        time.sleep(15)
    except TimeoutException:
        print("TimeoutException: Elemento de histórico não encontrado.")

def filtrar_e_contar(dados):
    linhas = dados.split('\n')
    resultados = []
    contador_numeros = 0
    for linha in linhas:
        try:
            numero = int(linha)
            if numero == 0:
                resultados.append(f"Sairam {contador_numeros} números antes do zero.")
                contador_numeros = 0
            else:
                contador_numeros += 1
        except ValueError:
            continue

    if contador_numeros > 0:
        resultados.append(f"Sairam {contador_numeros} números antes do zero.")
    with open("resultado1.txt", "w") as arquivo:
        for resultado in resultados:
            arquivo.write(resultado + "\n")

def verificar_condicao(dados):
    filtrar_e_contar(dados)

def salvar_segunda_linha(input_file, output_file):
    try:
        with open(input_file, 'r') as f_input:
            linhas = f_input.readlines()
            if len(linhas) >= 2:
                segunda_linha = linhas[1].strip()
                ultima_linha = ler_ultima_linha(output_file)
                if segunda_linha != ultima_linha:
                    with open(output_file, 'a') as f_output:
                        f_output.write(segunda_linha + "\n")
                    print("Segunda linha atualizada com sucesso em", output_file)
    except FileNotFoundError:
        print("Arquivo de entrada não encontrado.")

def ler_ultima_linha(nome_arquivo):
    try:
        with open(nome_arquivo, 'r') as f:
            linhas = f.readlines()
            return linhas[-1].strip() if linhas else ""
    except FileNotFoundError:
        print("Arquivo não encontrado.")
        return ""

def main():
    criar_tabela()
    input_file = "resultado1.txt"
    output_file = "novo_arquivo.txt"

    options = webdriver.FirefoxOptions()
    #options.headless = True
    driver = webdriver.Firefox(options=options)

    driver.get('https://blaze1.space/pt/games/double?modal=double_history_index')
    while True:
        coletar_dados(driver)
        salvar_segunda_linha(input_file, output_file)
        time.sleep(10)

    driver.quit()

if __name__ == "__main__":
    main()
