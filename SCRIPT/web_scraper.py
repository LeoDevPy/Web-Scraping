# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 13:10:22 2020

@author: lsouzadearau
"""

#Web Scraper 

#Imports 

import os #manipular sistema operacional
import re #manipular expressões regulares 
import csv  #manipular arquivos csv 
import pickle  #criar cash de acesso a pagina web  
import requests #fazer requisição a pagina 
from bs4 import BeautifulSoup #fazer o parse da pagina html

#Variavel com o endereço da página 
# Inicie o servidor web com o comando: python -m http.server 

PAGE = "http://localhost:8000/index.html"

#Função para extrair os dados 
def extrai_dados(cb): 
    
    #extraindo o nome do caro 
    str_name = cb.find('span', class_="car_name").text 
    
    #Extraindo o número de cilindros e converte para int 
    str_cylinders = cb.find('span', class_='cylinders').text 
    cylinders = int(str_cylinders)
    
    #Se o número de cilindros não for maior que zero, geramos mensagem de erro
    assert cylinders > 0, f"Esperando que o número de cilindros seja positivo e não {cylinders}"
    
    #Extraindo o peso do carro 
    str_weight = cb.find('span', class_='weight').text 
    
    #Removendo as vírgulas
    weight = int(str_weight.replace(',', ''))
    
    
    #Se o peso não for maior que zero, geramos a mensagem de erro
    assert weight > 0, f"Esperando que o peso seja positivo e não {weight}"
    
    # Extraindo a aceleração 
    acceleration = float(cb.find('span', class_='acceleration').text)
    
    #Se aceleração não for maior que zero, geramos mensagem de erro 
    assert acceleration > 0, f"Expecting acceleration to be positive and not {acceleration}"
    
    #Geramos um dicionário para cada linha extraída
    linha = dict(name=str_name, cylinders=cylinders,weight=weight, acceleration=acceleration)
    return linha
    
    
def processa_blocos_carros(soup):
    
    #Extraindo informações de repetidas divisões (tag div)
    car_blocks = soup.find_all('div', class_='car_block')
    
    #Lista vazia pra receber as linahs 
    linhas = []
    
    #Loop pelos blocos de dados de carros
    for cb in car_blocks:
        linha = extrai_dados(cb)
        linhas.append(linha)
        
    print(f"\n Temos {len(linhas)} linhas de dados retornadas do scraping de página!")
    
    #Imprime a primeira e a última linha 
    print("\nPrimeira linha copiada:")
    print(linhas[0])
    
    print("\núltima linha copiada:")
    print(linhas[-1])
    print("\n")
    
    
    #Grava o resultado em csv 
    with open("dados_copiados_v1.csv", "w") as f: 
        writer = csv.DictWriter(f, fieldnames = linha.keys())
        writer.writeheader()
        writer.writerows(linhas)
        
        
if __name__ == "__main__":
    
    #Arquivo para guardar os dados copiados em cache 
    filename = 'dados_copiados_v1.pickle'
    
    #Se o arquivo já existir, carregamos o arquivo 
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            print(f"\n Carregando o cache a partir do arquivo {filename}")
            result = pickle.load(f)
            
    #Se não, copiamos da página web 
    else:
       print(f"\n Copiando dados da página {PAGE}.")
       result = requests.get(PAGE)
       with open(filename, 'wb') as f:
           print(f"\nGravando o cache em {filename}")
           pickle.dump(result, f)
           
    #Se o status for diferente de 200, geramos mensagem de erro
    assert result.status_code == 200, f"Obteve status {result.status_code} verifique sua conexão!"
    
    # Obtém o texto da página 
    texto_web = result.text 
    
    #Faz o parser do texto da página 
    soup = BeautifulSoup(texto_web, 'html.parser')
    
    #Processa os dados de carros
    processa_blocos_carros(soup)
    
    
    
    
    
    
    
    
    
    
    
    
