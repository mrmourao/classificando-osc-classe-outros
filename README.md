# Reclassificando área de atuação "Outros" das OSCs utilizando Random Forest Classifie.
Com base no repositório de classificação das áreas de atuação das OSCs, este repositório está sendo criado para reclassificar as áreas de atuação consideradas como "Outros" na classificação original, logo não haverá a avaliação dos resultados.

Para treinamento do modelo deste projeto, foram retirados dos dados todas as OSCs que tinham mais de uma área de atuação, juntamente com todas as OSCs que haviam sido classificadas como "10 - Outros" ou "11 - Outras atividades associativas".

Devido ser uma classificação onde não temos a sua resposta para avaliar o modelo, será considerado a acurácia do modelo desenvolvido anteriormente, com o percentual de 98% de acerto.

Neste repositório, será disponibilizado todo o conteúdo necessário para a criação do modelo preditivo e uma classificação em massa, onde como resposta será gerado um arquivo .json com os resultados.

## Versão 1.0

### Estrutura do projeto
- App
	- dados
		* entrada 
		
              dados_gerais.csv /* arquivo de dados gerais com as características das OSCs */
              area_atuacao.csv /* arquivo com os dados de classificação das áreas de atuação de cada OSC. */
              dados.csv /* arquivo com os dados para o modelo classificar. */
    
		* saída
		
              local onde serão gerados os arquivos: resultado.json com todos os resultados da classificação, o aquivo com o agrupamento das áreas por OSC, label encoder utilizado para treinar o modelo, o modelo treinado e os arquivos com as colunas removidas durante todo o processo.
				
	- modelos
		* modelos.cfg 
		
			Arquivo de configuração dos diretórios e parâmetros necessários para geração do modelo:
				
				DADOS_GERAIS = informar o nome do arquivo dos dados gerais, que possui as características das OSCs.
 
				AREA_ATUACAO = informar o nome do arquivo de área de atuação, que possui a classificação da OSC.

				AREA_AGRUPADA = informar o nome do arquivo a ser gerado com o agrupamento de todas as áreas de atuação.

				MODELO = informar o nome do modelo que será gerado.

				LABEL_ENCODER = informar o nome do label encoder a ser salvo no momento do treino do modelo.

	 * modelos.log
	 
	 		Arquivo com todos os logs do processamento da criação e treinamento.
  
	
	- utils
	
		* log_factory.py
	
			arquivo gerador de logs
  
	- classificacao
	
		* classificacao.cfg
			
			arquivo de configuração utilizado na classificação
	
              MASSA_DADOS = informar o nome do arquivo que contém os dados que serão aplicados no modelo para previsão da área de atuação.
        
              MODELO = informar o nome do modelo gerado pelo processo de geração de modelo, mesmo nome informado no arquivo 'modelos.cfg'.
	
              LABEL_ENCODER = informar o nome do label encoder gerado pelo processo de geração de modelo, mesmo nome informado no arquivo 'modelos.cfg'.
        
  * classificacao.log
      
        arquivo com os logs de todo o processo de classificação

- main.cfg
	
		arquivo de configuração para ativar os módulos do aplicativos, onde os parâmetros ProcessaAgrupamentoAreaAtuacao, GeraModelo e GeraClassificacao devem ser referenciados com os valores de True ou False de acordo com a necessidade. Para o primeiro processamento, todos os valores devem possuir o valor de True, para que os modelos e suas dependências sejam geradas.

- main.py

		arquivo python que inicia toda a aplicação, após configuração de todos os arquivos, basta rodar este arquivo utilizando, por exemplo, o	comando ‘python main.py’ que a aplicação será executada.

- modelos.py

		arquivo python com os códigos necessários para a geração do agrupamento das área de atuação, o modelo radom forest e o label encoder.

- classificacao.py
	
		arquivo python com os códigos necessários para classificar a massa de dados e gerar o resultado com a previsão.

- extracao_dados.py
  
      arquivo com um código extra, para auxiliar na extração da classe "Outros" do dataframe original e montar um arquivo de dados pronto para aplicar ao modelo. Para a sua execução basta chamar o comando 'python extracao_dados.py' que será gerado um arquivo na pasta de saída de dados com o nome "dados_extraidos.csv", agora basta colocar este arquivo na pasta de entrada de dados e configurar no arquivo de classificacao.cfg o parâmetro MASSA_DADOS.

# Requisitos
- Python 3.6
- Pandas
- Pickle
- Sklearn
- Tqdm

### Instalando os requisitos

	pip install -r requirements.txt
