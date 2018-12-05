# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------    
# Importes das bibliotecas utilizadas

import logging
import time
import pandas as pd
import pickle

from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from utils.log_factory        import Log
from os.path                  import dirname, abspath, join
from tqdm 					  import tqdm

import warnings
warnings.filterwarnings("ignore")

#------------------------------------------------------------------------------    
# Globals variables
PATH = dirname(abspath(__file__))
#------------------------------------------------------------------------------    

class ProcessaAgrupamentoAreaAtuacao():

	''' Algumas ONGs possuem mais de um tipo de area de atuacao, por isso, estou agrupando as areas de
	        cada ONG criando assim a possibilidade de ser classificada em mais de uma area '''

	def processa():

		log = ''
		
		begin = time.time()

		# iniciando o log
		logPath = join(PATH,"modelos","modelos.log")
		Log.setLog("agrupamento", logPath)
		log = logging.getLogger("agrupamento")

		log.info('Iniciando o processo de agrupamento das areas de atuacao')
		log.info("Lendo o arquivo de configuracao")
		config = readConfig(join(PATH,"modelos","modelos.cfg"))

		# definindo os tipos de dados para importacao
		dtype={"id_area_atuacao":object, "id_osc": int, "cd_area_atuacao": int, "cd_subarea_atuacao": object, 
			   "ft_area_atuacao": object, "bo_oficial": object, "tx_nome_outra": object}

		log.info("Importando os dados do arquivo de area de atuacao")
		caminho_arquivo = join(PATH,"dados","entrada",config["AREA_ATUACAO"])
		df_area_atuacao = pd.read_csv(caminho_arquivo, sep=";", 
			encoding='utf-8', error_bad_lines=False, dtype=dtype)

		log.info("Realizando alguns tratamentos nos dados importados")

		""" removendo o tipo de area de atuacao igual a 8, devido somente existir 3 registros no arquivo de area de atuacao e so 1
	        como chave para dados gerais: para conferencia utilizar os codigos abaixo
	        df_area_atuacao[(df_area_atuacao.cd_area_atuacao == 8)] df[(df.id_osc == 521832)]
	        df_area_atuacao.groupby('cd_area_atuacao').id_area_atuacao.count()"""
		df_area_atuacao.drop(df_area_atuacao[(df_area_atuacao.cd_area_atuacao == 8)].index, inplace=True)

		""" removendo deixando no df de area de atuacao, somente o codigo da area, sendo a informacao que sera utilizada
	        para a classificacao """
		df_area_atuacao.drop(columns=["id_area_atuacao","cd_subarea_atuacao","ft_area_atuacao","bo_oficial","tx_nome_outra"]
	                         ,inplace=True)
		
		df_area_atuacao.drop_duplicates(inplace=True)

		
		log.info("Iniciando o agrupamento")
		series_cd_area = pd.Series()
		old_id_osc = 0
		for id_osc in tqdm(df_area_atuacao.id_osc.sort_values()):
			if old_id_osc == id_osc:
				continue
			else:
				old_id_osc = id_osc
			
			area = str(df_area_atuacao[df_area_atuacao.id_osc == id_osc].cd_area_atuacao.sort_values().values).replace(' ','').replace('[','').replace(']','')
			
			s = pd.Series([area], index=[id_osc])
			series_cd_area = series_cd_area.append(s, ignore_index=False)
		
		df_cd_area = pd.DataFrame(data=series_cd_area)
		df_cd_area.reset_index(inplace=True)
		df_cd_area.columns = ["id_osc", "cd_area_atuacao"]
		
		arq = open(join(PATH,'dados','saida',config["AREA_AGRUPADA"]),'wb')
		pickle.dump(df_cd_area, arq)
		arq.close()
		
		end = time.time() - begin
		log.info('Fim do processo de agrupamento. Total de %s decorrido.' % str(end))
		

#------------------------------------------------------------------------------

class Modelo():

	''' Algumas ONGs possuem mais de um tipo de area de atuacao, por isso, estou agrupando as areas de
	        cada ONG criando assim a possibilidade de ser classificada em mais de uma area '''

	def gera_random_forest():

		log = ''
		
		begin = time.time()

		# iniciando o log
		logPath = join(PATH,"modelos","modelos.log")
		Log.setLog("gera_modelo", logPath)
		log = logging.getLogger("gera_modelo")

		log.info('Iniciando o processo de geracao do modelo random forest')
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
		df.cd_area_atuacao = df.cd_area_atuacao.apply(int)
		df = df[(df.cd_area_atuacao < 10)]
		

		log.info('Fim da uniao. Total de %s decorrido' % str(time.time() - ini))
		
		#------------------------------------------------------------------------------
		log.info('Iniciando a remocao das colunas 100% nulas')
		ini = time.time()
		""" aplicando a primeira limpeza no df, eliminando as colunas 100% nulas """
		colunas = []
		for coluna in df.columns:
			qte_null = df[coluna].isnull().sum()
			perc_null = round(qte_null/len(df[coluna]), 2)

			if perc_null == 1.0:
				colunas.append(coluna)

		# armazenando as colunas excluidas
		arq_colunas_excluidas = open(join(PATH,'dados','saida','colunasRemovidas100PorcentoNulas.txt'),"w")
		arq_colunas_excluidas.write(str(colunas))
		arq_colunas_excluidas.close()

		# removendo as colunas do dataframe
		df = df.drop(columns=colunas, axis=0)

		log.info('Fim do processo. Total de %s decorrido' % str(time.time() - ini))

		#------------------------------------------------------------------------------

		log.info('Iniciando a remocao das colunas nao relevantes')
		ini = time.time()
		""" avaliando pontualmente cada variável do df definindo a relevancia 
		- retirada ft_link_relatorio_auditoria pois só havia um tipo de registro e o restante nulo
		- retirada ft_link_demonstracao_contabil pois só havia um tipo de registro e o restante nulo
		- retirada bo_nao_possui_sigla_osc pois só havia um tipo de registro e o restante nulo
		- retirada bo_nao_possui_link_estatuto_osc pois só havia um tipo de registro e o restante nulo
		- retirada a coluna da código da sub área de atuação, pois é uma informação vinculada a área de atuação. """

		colunas_removidas = ["id_osc","bo_nao_possui_sigla_osc","bo_nao_possui_link_estatuto_osc","dt_fundacao_osc"
		,"tx_razao_social_osc","tx_nome_fantasia_osc","ft_link_relatorio_auditoria","ft_link_demonstracao_contabil"
		,"ft_classe_atividade_economica_osc","ft_natureza_juridica_osc"]

		colunas_texto = ["ft_link_estatuto_osc","ft_historico","ft_finalidades_estatutarias"
		,"ft_nome_responsavel_legal","ft_razao_social_osc","ft_nome_fantasia_osc","ft_logo","ft_missao_osc"
		,"ft_visao_osc","ft_fundacao_osc","ft_sigla_osc","ft_resumo_osc","ft_situacao_imovel_osc"
		,"ft_ano_cadastro_cnpj"]

		# removendo as colunas do dataframe
		df.drop(columns=colunas_removidas, axis=0, inplace=True)

		# armazenando as colunas excluídas
		arq_colunas_excluidas = open(join(PATH,'dados','saida','colunasRemovidasAposAvaliacao.txt'),"w")
		arq_colunas_excluidas.write(str(colunas))
		arq_colunas_excluidas.close()

		log.info('Fim do processo. Total de %s decorrido' % str(time.time() - ini))

		#------------------------------------------------------------------------------

		log.info('Iniciando o tratamento com label_encoder e preparando o df')
		ini = time.time()

		dic = {}
		log.info('Aplicando o LabelEncoder')
		for col in colunas_texto:
			df[col] = df[col].fillna("")
			le = preprocessing.LabelEncoder()
			tmp  = le.fit(df[col])
			dic[col] = tmp        
			df[col] = tmp.transform(df[col])

		log.info('Salvando o LabelEncoder para aplicar em producao')
		pickle.dump(dic,open(join(PATH,"dados","saida",config['LABEL_ENCODER']),'wb'))

		log.info('Substituindo os valores nulos por -1')
		df.fillna(-1, inplace=True)

		log.info('Convertendo todos os dados do df para int')
		for col in df.columns:
			df[col] = df[col].apply(int)

		log.info('Fim do processo. Total de %s decorrido' % str(time.time() - ini))

		#------------------------------------------------------------------------------

		log.info('Iniciando a remocao das colunas com alto nivel de correlacao')
		ini = time.time()

		log.info('criando uma matriz com a correlacao entre todas as variaveis do df')
		dim = df.shape[1]
		matrix = [[0]*dim for i in range(dim)]
		for i in range(dim):
			for j in range(dim):
				matrix[i][j] = df.iloc[:,i].corr(df.iloc[:,j])

		df_matrix = pd.DataFrame(matrix, columns=df.columns, index=df.columns)

		log.info('Identificando as correlações acima de 0.9 ou menores de -0.9 e removendo as colunas do df')
		colunas_alto_nivel_corr = []
		arquivo_colunas_removidas = open(join(PATH,'dados','saida','colunasRemovidasDevidoAltoNivelCorrelacao.txt'), 'w')

		for linha, valor in df_matrix.iterrows():
			for coluna in df_matrix.columns:
				if linha == coluna:
					continue

				if valor[coluna] >= 0.9 or valor[coluna] <= -0.9:
					tx = "Correlação entre: {:s} e {:s} = {:f} \n".format(linha,coluna,valor[coluna])
					arquivo_colunas_removidas.write(tx)
					colunas_alto_nivel_corr.append(coluna)

		arquivo_colunas_removidas.close()
		df.drop(columns=set(colunas_alto_nivel_corr), inplace=True)

		log.info('Fim do processo. Total de %s decorrido' % str(time.time() - ini))

		#------------------------------------------------------------------------------

		log.info('Separando os dados de treino e teste em 70% para treino e 30% para teste')
		ini = time.time()

		X_treino, X_teste, y_treino, y_teste = train_test_split(df, df.cd_area_atuacao, test_size=0.3)

		log.info('Retirando a variavel de resposta do df de treino e teste')
		X_treino = X_treino.iloc[:,1:]
		X_teste = X_teste.iloc[:,1:]

		log.info('Fim do processo. Total de %s decorrido' % str(time.time() - ini))

		#------------------------------------------------------------------------------

		log.info('Treinando o modelo de classificacao utilizando o algoritmo RandomForestClassifier da biblioteca sklearn')
		ini = time.time()

		log.info('Criando o modelo')
		rf = RandomForestClassifier(n_estimators= 200, min_samples_split = 10, min_samples_leaf = 2, 
		                            max_features = 'sqrt', max_depth = 50, bootstrap = True)

		log.info('Treinando o modelo')
		rf.fit(X_treino, y_treino)

		log.info('Salvando o modelo para ser usado em producao')
		file = open(join(PATH,"dados","saida",config['MODELO']),'wb')
		pickle.dump(rf,file)
		file.close()

		log.info('Fim do processo. Total de %s decorrido' % str(time.time() - ini))

		#------------------------------------------------------------------------------
		end = time.time() - begin
		log.info('Fim do processo de geracao do modelo random forest. Total de %s decorrido.' % str(end))
		
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