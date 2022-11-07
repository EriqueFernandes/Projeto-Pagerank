import numpy as np
import random
import pandas as pd
import requests
from bs4 import BeautifulSoup

def internet_example(tamanho: int, probabilidade_ligacao: float):
    M = np.zeros((tamanho, tamanho))
    for i in range(tamanho):
        for j in range(tamanho):
            r = random.random()
            if r < probabilidade_ligacao:
                M[i,j] = 1
    
    soma = sum(M)
    for i in range(tamanho):
        if soma[i] == 0:
            continue
        M[:,i] = M[:,i] / soma[i]
    
    return M

def page_rank(matriz_internet, d: float = 0.85, epsilon: float = 0.00001):
    N = matriz_internet.shape[0]
    E = np.ones(matriz_internet.shape)
    controle = True
    n_iteracoes = 0
    
    #sem amortecimento
    if d == None: d = 1
    
    M_estrela = d * matriz_internet + (1 - d)/N * E
    
    # definimos x_0 = 1/N 
    x = [None, 1/N * np.ones((N, 1))]
    
    # na iteracao t, temos que x_(t+1) = M_estrela * x_t
    # quando absoluto(x_t+1 - x_t) < epsilon, teremos que x[1] é o pagerank
    while controle:
        # x[0] recebe antigo x[1]
        # x[1] recebe multiplicacao de M_estrela com x[1]
        x[0], x[1] = x[1], np.dot(M_estrela , x[1])
        n_iteracoes += 1
        
        controle = False
        
        for i in range(x[0].shape[0]):
            if x[1][i]  - x[0][i] > epsilon:
                controle = True
        
    return x[1], n_iteracoes
    
def pega_links(url):
    data = requests.get(url).text
    html = BeautifulSoup(data, "html.parser")
    
    lista_links = []
    for link in html.findAll("a"):
        try:
            if link["href"].startswith("http"):
                lista_links.append(link["href"])
        except KeyError:
            continue
    
    lista_definitiva = []
    for link in lista_links:
        dados = requests.get(url).text
        html_link = BeautifulSoup(dados, "html.parser")
        novos_links = html_link.findAll("a")
        for lk in novos_links:
            try:
                if lk["href"].startswith("http"):
                    lista_definitiva.append(lk["href"])
            except KeyError:
                continue
    
    dicionario = {}
    for elemento in lista_definitiva:
        try:
            dicionario[elemento] += 1
        except KeyError:
            dicionario[elemento] = 1
    
    return dicionario
    
    
link = "https://pt.wikipedia.org/wiki/M%C3%A5neskin"
    
x = pega_links(link)
print(x)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    