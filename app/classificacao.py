# -*- coding: utf-8 -*-

import pickle
import json
import logging
import time
import pandas as pd

from tqdm import tqdm
from utils.log_factory        import Log
from os.path import dirname, abspath, join

import warnings
warnings.filterwarnings("ignore")

#------------------------------------------------------------------------------    
# Globals variables
PATH = dirname(abspath(__file__))
#------------------------------------------------------------------------------   
class Classificacao():
	
	def processa():

		log = ''
		
		begin = time.time()

		# iniciando o log
		logPath = join(PATH,"classificacao","classificacao.log")
		Log.setLog("classificacao", logPath)
		log = logging.getLogger("classificacao")

		log.info('Iniciando o processo de classificacao da massa')
		log.info("Lendo o arquivo de configuracao")
		config = readConfig(join(PATH,"classificacao","classificacao.cfg"))

		log.info("Carregando o arquivo de label encoder")
		file = open(join(PATH,'dados','saida',config['LABEL_ENCODER']),'rb')
		le = pickle.load(file)
		file.close()

		log.info("Carregando o modelo random forest")
		file = open(join(PATH,'dados','saida',config['MODELO']),'rb')
		rf = pickle.load(file)
		file.close()

		log.info("Carregando o arquivo de dados")
		df = pd.read_csv(join(PATH,'dados','entrada',config['MASSA_DADOS']))

		resultado = {}
		resultado["classificacao"] = []

		log.info("Iniciando a classificacao")
		for i in tqdm(df.iterrows()):
			classificacao = Classificacao.busca_area(i[1],le,rf)
			resultado["classificacao"].append(classificacao)

		log.info("Salvando o arquivo de resultado")
		file = open(join(PATH,'dados','saida','resultado.json'),'w')
		json.dump(resultado,file,default=str)
		file.close()

		end = time.time() - begin
		log.info('Fim do processo de classificacao. Total de %s decorrido.' % str(end))

		
	def busca_area(consulta,le,rf):

		cd_natureza_juridica_osc = str(consulta.cd_natureza_juridica_osc).replace("nan",'')
		ft_razao_social_osc = str(consulta.ft_razao_social_osc).replace("nan",'')
		ft_nome_fantasia_osc = str(consulta.ft_nome_fantasia_osc).replace("nan",'')
		ft_fundacao_osc = str(consulta.ft_fundacao_osc).replace("nan",'')
		cd_classe_atividade_economica_osc = str(consulta.cd_classe_atividade_economica_osc).replace(".0","").replace("nan",'')

		erros = {}

		if cd_natureza_juridica_osc == '':
			cd_natureza_juridica_osc = -1
		else:
			try:
				cd_natureza_juridica_osc = int(cd_natureza_juridica_osc)
			except Exception as e :
				erros["cd_natureza_juridica_osc"] = {}
				erros["cd_natureza_juridica_osc"]['mensagem'] = 'Nao foi possivel converter o valor informado, verifique caracter diferente de [0-9]'
				erros["cd_natureza_juridica_osc"]['exception'] = str(e)


		if ft_razao_social_osc == '':
			ft_razao_social_osc = -1
		else:
			try:
				fit = le['ft_razao_social_osc']
				ft_razao_social_osc = fit.transform([ft_razao_social_osc])[0]
			except Exception as e:
				erros["ft_razao_social_osc"] = {}
				erros["ft_razao_social_osc"]['mensagem'] = '''Nao foi possivel aplicar o label encoder para o valor informado, caso seja um novo valor para o campo, sera necessario treinar novamente o modelo'''
				erros["ft_razao_social_osc"]['exception'] = str(e)

		if ft_nome_fantasia_osc == '':
			ft_nome_fantasia_osc = -1
		else:
			try:
				fit = le['ft_nome_fantasia_osc']
				ft_nome_fantasia_osc = fit.transform([ft_nome_fantasia_osc])[0]
			except Exception as e :
				erros["ft_nome_fantasia_osc"] = {}
				erros["ft_nome_fantasia_osc"]['mensagem'] = '''Nao foi possivel aplicar o label encoder para o valor informado, caso seja um novo valor para o campo, sera necessario treinar novamente o modelo'''
				erros["ft_nome_fantasia_osc"]['exception'] = str(e)

		if ft_fundacao_osc == '':
			ft_fundacao_osc = -1
		else:
			try:
				fit = le['ft_fundacao_osc']
				ft_fundacao_osc = fit.transform([ft_fundacao_osc])[0]
			except Exception as e :
				erros["ft_fundacao_osc"] = {}
				erros["ft_fundacao_osc"]['mensagem'] = '''Nao foi possivel aplicar o label encoder para o valor informado, caso seja um novo valor para o campo, sera necessario treinar novamente o modelo'''
				erros["ft_fundacao_osc"]['exception'] = str(e)

		if cd_classe_atividade_economica_osc == '':
			cd_classe_atividade_economica_osc = -1
		else:
			try:
				cd_classe_atividade_economica_osc = int(cd_classe_atividade_economica_osc)
			except Exception as e :
				erros["cd_classe_atividade_economica_osc"] = {}
				erros["cd_classe_atividade_economica_osc"]['mensagem'] = 'Nao foi possivel converter o valor informado, verifique caracter diferente de [0-9]' 
				erros["cd_classe_atividade_economica_osc"]['exception'] = str(e)

		previsao = ''
		if erros == {}:
			try:
				X_producao = [[cd_natureza_juridica_osc,ft_razao_social_osc,ft_nome_fantasia_osc,ft_fundacao_osc,cd_classe_atividade_economica_osc]]
				previsao = rf.predict(X_producao)
			except Exception as e :
				erros["erro_ao_aplicar_modelo"] = {}
				erros["erro_ao_aplicar_modelo"]['mensagem'] = 'Nao foi possivel aplicar o modelo para os valor informados.'
				erros["erro_ao_aplicar_modelo"]['exception'] = str(e)

		resultado = {}
		resultado['id_osc'] = consulta.id_osc
		resultado['area atuacao'] = list(previsao)
		resultado['erros'] = erros
		resultado['status'] = 'OK' if erros == {} else 'FALHA'
		return resultado

#------------------------------------------------------------------------------
 # Metodo auxiliar para ler o arquivo de configuracao  
def readConfig(filepath):
	file = open(join(PATH,filepath))
	dict_config = {}

	for line in file:
		key, value = line.replace(" ","").replace("\n","").split("=")
		dict_config[key] = value

	return dict_config

#------------------------------------------------------------------------------