# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------    
# Importes das bibliotecas utilizadas

import logging
import time
import pandas as pd
import pickle

from utils.log_factory        import Log
from os.path                  import dirname, abspath, join

import warnings
warnings.filterwarnings("ignore")

#------------------------------------------------------------------------------    
# Globals variables
PATH = dirname(abspath(__file__))
#------------------------------------------------------------------------------    

""" metodo utilizado para extrair do arquivo de dados gerais, somente os 
    dados de determinada area de atuacao, os dados serao exportados em csv
    no formato necessario para o modelo classificar.
    
    para que o metodo funcione corretamente e necessario que o processo de
    agrupamento de area de atuacao ja tenha sido feito e exista o arquivo
    de dados gerais configurado no arquivo 'modelo.cfg' """
def extrai_dados_por_area_atuacao(areas):

	log = ''

	begin = time.time()

	# iniciando o log
	logPath = join(PATH,"extracao_dados.log")
	Log.setLog("extracao_dados", logPath)
	log = logging.getLogger("extracao_dados")

	log.info('Iniciando o processo de extracao de dados')
	log.info("Lendo o arquivo de configuracao")
	config = readConfig(join(PATH,"modelos","modelos.cfg"))

	#------------------------------------------------------------------------------

	# definindo os tipos de dados para importação
	dtype={"id_osc": int, "cd_natureza_juridica_osc": object, 
		"ft_natureza_juridica_osc": object, "tx_razao_social_osc": object, 
		"ft_razao_social_osc": object, "tx_nome_fantasia_osc": object, 
		"ft_nome_fantasia_osc": object, "im_logo": object, "ft_logo": object, 
		"tx_missao_osc": object, "ft_missao_osc": object, "tx_visao_osc": object, 
		"ft_visao_osc": object, "dt_fundacao_osc": object, 
		"ft_fundacao_osc": object, "dt_ano_cadastro_cnpj": object, 
		"ft_ano_cadastro_cnpj": object, "tx_sigla_osc": object, 
		"ft_sigla_osc": object, "tx_resumo_osc": object, "ft_resumo_osc": object, 
		"cd_situacao_imovel_osc": object, "ft_situacao_imovel_osc": object, 
		"tx_link_estatuto_osc": object, "ft_link_estatuto_osc": object, 
		"tx_historico": object, "ft_historico": object, 
		"tx_finalidades_estatutarias": object, "ft_finalidades_estatutarias": object, 
		"tx_link_relatorio_auditoria": object, "ft_link_relatorio_auditoria": object, 
		"tx_link_demonstracao_contabil": object, "ft_link_demonstracao_contabil": object, 
		"tx_nome_responsavel_legal": object, "ft_nome_responsavel_legal": object, 
		"cd_classe_atividade_economica_osc": object, "ft_classe_atividade_economica_osc": object, 
		"bo_nao_possui_sigla_osc": object, "bo_nao_possui_link_estatuto_osc": object}

	log.info('Iniciando a importacao dos dados gerais')
	ini = time.time()

	# importando os dados do arquivo de dados gerais
	df_dados_gerais = pd.read_csv(join(PATH,"dados","entrada",config["DADOS_GERAIS"]), sep=";",
				encoding='utf-8', error_bad_lines=False, dtype=dtype)

	log.info('Fim da importacao dos dados gerais. Total de %s decorrido' % str(time.time() - ini))

	#------------------------------------------------------------------------------

	log.info('Iniciando a importacao das areas de atuacao agrupada')
	ini = time.time()

	""" unindo os dataframes de area de atuacao e dados gerais pela chave de id_osc """
	arq = open(join(PATH,'dados','saida',config['AREA_AGRUPADA']),'rb')
	df_cd_area = pickle.load(arq)
	arq.close()

	log.info('Fim da importacao das areas de atuacao agrupada. Total de %s decorrido' % str(time.time() - ini))

	log.info('Iniciando a uniao dos dados gerais com a area de atuacao agrupada')
	ini = time.time()

	df = pd.merge(df_cd_area,df_dados_gerais, on="id_osc")

	""" retira as OSCs que tenham mais de uma area de atuacao e as que sao classificadas
		como outras (10 e 11) """
	log.info('Extraindo os dados atraves das areas informadas')
	df.cd_area_atuacao = df.cd_area_atuacao.apply(int)
	df = df[(df.cd_area_atuacao.isin(areas))]

	""" realizando um slice para exportar somente as colunas utilizadas na classificacao do modelo """
	df = df.loc[:,['id_osc','cd_natureza_juridica_osc','ft_razao_social_osc','ft_nome_fantasia_osc'
				  ,'ft_fundacao_osc','cd_classe_atividade_economica_osc']]
	
	""" removendo duplicadas caso ocorra """
	df.drop_duplicates(inplace=True)

	log.info('Salvando em arquivo os dados extraidos')
	df.to_csv(join(PATH,'dados','saida','dados_extraidos.csv'),index=False)
	
	log.info('Fim da uniao. Total de %s decorrido' % str(time.time() - ini))

	end = time.time() - begin
	log.info('Fim da execucao. Total de %s decorrido.' % str(end))

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
# Inicio do metodo main

if __name__ == "__main__":
	# atribua a variavel areas as classes que deseja extrair dos dados gerais
    areas = [10]
    extrai_dados_por_area_atuacao(areas)
#------------------------------------------------------------------------------