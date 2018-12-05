# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------    
# Importes das bibliotecas utilizadas

import logging
import time

from classificacao             import Classificacao
from modelos                   import ProcessaAgrupamentoAreaAtuacao, Modelo
from utils.log_factory         import Log
from os.path                   import dirname, abspath, join

import warnings
warnings.filterwarnings("ignore")

#------------------------------------------------------------------------------    
# Variaveis Globais
PATH = dirname(abspath(__file__))

#------------------------------------------------------------------------------    
# Metodo Main
def main():
    
    # Iniciando o tempo de execucao da aplicacao
    begin = time.time()
    
    # Iniciando o log
    logPath = join(PATH,"main.log")
    Log.setLog(__name__, logPath)
    log = logging.getLogger(__name__)
    log.info("Iniciando a aplicacao")
    
    log.info("Lendo o arquivo de configuracao")
    config = readConfig("main.cfg")
    
    if config["ProcessaAgrupamentoAreaAtuacao"]:
        log.info("Chamando o metodo de agrupamento das areas de atuacao por osc")
        ini = time.time()
        
        ProcessaAgrupamentoAreaAtuacao.processa()
        
        log.info('Fim do processo de agrupamento das areas de atuacao. Total de %s decorrido.' % str(time.time()-ini))
        
    if config["GeraModelo"]:
        log.info("Chamando o processamento para geracao do modelo de classificacao")
        ini = time.time()
        
        Modelo.gera_random_forest()
        
        log.info('Fim do processamento da geracao do modelo. Total de %s decorrido.' % str(time.time()-ini))
        
    if config["GeraClassificacao"]:
        log.info("Chamando o processamento de classificacao")
        ini = time.time()
        
        Classificacao.processa()

        log.info('Fim do processamento da classificacao. Total de %s decorrido.' % str(time.time()-ini))
        
    end = time.time() - begin
    log.info('Fim da execucao. Total de %s decorrido.' % str(end))
    
#------------------------------------------------------------------------------    
# Metodo Auxiliar

def readConfig(filepath):
    
    file = open(join(PATH,filepath))
    
    dic = {}
    for line in file:
        key, value = line.replace(" ","").split("=")
        dic[key] = (True if "True" in value else False)
           
    return dic

#------------------------------------------------------------------------------    
# Inicio do metodo main

if __name__ == "__main__":
    main()

#------------------------------------------------------------------------------