# Descrição do problema.
 
A Rossmann opera mais de 3.000 drogarias em 7 países europeus. Atualmente, os gerentes de loja da Rossmann têm a tarefa de prever suas vendas diárias com até seis semanas de antecedência. As vendas da loja são influenciadas por muitos fatores, incluindo promoções, competição, feriados escolares e estaduais, sazonalidade e localidade. Com milhares de gerentes individuais prevendo vendas com base em suas circunstâncias únicas, a precisão dos resultados pode ser bastante variada. E um dos desejos desta empresa é a previsão da venda futura de 6 semanas das suas 1115 lojas. Os dados disponíveis por ela contém as seguintes informações: 
 
* **Id** - an Id that represents a (Store, Date) duple within the test set
* **Store [T]** - a unique Id for each store
* **Sales [T]** - the turnover for any given day (this is what you are predicting)
* **Customers [T]** - the number of customers on a given day
* **Open [T]** - an indicator for whether the store was open: 0 = closed, 1 = open
* **StateHoliday [T]** - indicates a state holiday. Normally all stores, with few exceptions, are closed on state holidays. Note that all schools are closed on public holidays and weekends. a = public holiday, b = Easter holiday, c = Christmas, 0 = None
* **SchoolHoliday [T]** - indicates if the (Store, Date) was affected by the closure of public schools
* **StoreType [S]** - differentiates between 4 different store models: a, b, c, d
* **Assortment [S]** - describes an assortment level: a = basic, b = extra, c = extended
* **CompetitionDistance [S]** - distance in meters to the nearest competitor store
* **CompetitionOpenSince[Month/Year] [S]** - gives the approximate year and month of the time the nearest competitor was opened
* **Promo [T]** - indicates whether a store is running a promo on that day
* **Promo2 [S]** - Promo2 is a continuing and consecutive promotion for some stores: 0 = store is not participating, 1 = store is participating
* **Promo2Since[Year/Week] [S]** - describes the year and calendar week when the store started participating in Promo2
* **PromoInterval [S]** - describes the consecutive intervals Promo2 is started, naming the months the promotion is started anew. E.g. "Feb,May,Aug,Nov" means each round starts in February, May, August, November of any given year for that store
 
# Objetivo.
 
Sendo assim, esse trabalho visa realizar a predição de vendas dessas lojas através de um modelo de machine learning e a criação de um api que retorne as previsões feitas por ele.  
 
# Metodologia
 
Este projeto será baseado no processo padrão Cross-industry para mineração de dados (CRISP-DM). Uma ideia padrão sobre projeto de ciência de dados pode ser linear: preparação de dados, modelagem, avaliação e implantação. No entanto, quando usamos a metodologia CRISP-DM, um projeto de ciência de dados se torna uma forma circular. Mesmo quando termina em Deployment, o projeto pode ser reiniciado novamente pela Business Understanding. 
 
 
<p align="center">
    <img src="https://upload.wikimedia.org/wikipedia/commons/b/b9/CRISP-DM_Process_Diagram.png" alt="Kitten" title="A cute kitten" width="430" height="430" />
</p>
 
Pode ajudar a evitar que o cientista de dados pare em uma etapa específica e perca tempo com ela. Quando todo o projeto estiver concluído, o cientista de dados pode retornar à etapa inicial e fazer todas as etapas novamente. Portanto, o objetivo principal é seguir círculos conforme a necessidade. 
 
# Pipeline
 
* Tratamento dos dados.
* Análise dos dados.
* Preparação dos dados.
* Feature Engineering.
* Modelagem dos modelos de Machine Learning.
* Ajuste dos hiperparâmetros.
* Avaliação do melhor modelo. 
* Deploy do modelo.
 
# Aquisição dos dados.
 
Esse conjunto de dados foram retirados do Kaggle no seguinte link https://www.kaggle.com/c/rossmann-store-sales.  
  
# Descrição do projeto

O Projeto foi desenvolvido em duas partes principais:
 
* Parte 1: Analisar os dados obtidos, encontrar o melhor modelo de machine learning para a solução do problema.
* Parte 2: Deploy do melhor modelo encontrado e o seu teste. 
  
### Parte 1.
Essa parte do projeto foi realizada nas seguintes etapas :
* Tratamento dos dados: Tratamento dos dados faltantes, outliers e unir os conjuntos Train e Test. Teve algumas variáveis criadas para dar suporte nas análises que serão feitas.
* Descrição dos dados: É visto como as vendas se relacionam com o tempo e com as demais variáveis.
* Parte 1 Modification dataset : Nesta parte será encontrado a melhor maneira de representar as variáveis discretas e selecionar as melhores para o treinamento do modelo.
* Parte 2 Modification dataset : Continuação do notebook Parte 1 Modification dataset.
* models: Tuning de diversos modelos de machine learning e a avaliação deles, para que assim possa ser escolhido algum para o deploy.
 
 
**Cada etapa realizada possui um arquivo e cada um se encontram em uma pasta chamada Notebook**
 
### Parte 2.
 
O deploy do projeto foi realizado basicamente em 3 seções :
* Primeira seção: Criação de uma classe para processar os dados que chegam no API.
* Segunda seção: Testar a classe criada para processar os dados e salvar o modelo criado em disco.
* Terceira seção: Criação do API e de um notebook para testá-lo.
 
Estas seções se encontram nos seguintes arquivo .py
 
* Store_v1 : Classe utilizada para processar os dados para treinar o modelo que foi levado em produção.
* Store_v2 : Classe utilizada para processar os dados que chegam no API criado.
* teste_v1 : Testar a classe criada no arquivo Store_v1
* teste_v2 : Testar a classe criada no arquivo Store_2 e treinar e salvar em disco o modelo de machine learning que foi levado para produção.
* model_api_store: API criado através do flask para realizar o deploy do modelo.
 
**Todos estes arquivos se encontram na pasta API, aqueles contém as classes para processar os dados, estão no seguinte caminho \api\lojas.**
  
# Resultados 
 
### Análise de dados.
 
* Os principais fatores que se destacaram nas análises feitas foram que a venda é maior em determinados dias específicos dos meses. A maior venda acontece em dezembro e isso se deve por causa dos feriados, conforme esta sendo mostrado nos gráficos abaixo.
 
 <p align="center">
    <img src="https://user-images.githubusercontent.com/28810281/166516530-45b9e2fe-222b-4162-b888-243ba75edf66.png" alt="vendas_mes" title="vendas_mes" width="830" height="430" />
</p>

<p align="center">
    <img src="https://user-images.githubusercontent.com/28810281/166594652-bea6dd16-e2c7-44c6-9f9c-6c33ce939535.png" alt="vendas_mes" title="vendas_mes" width="830" height="430" />
</p>

<p align="center">
    <img src="https://user-images.githubusercontent.com/28810281/166591315-6be8068d-2c24-4c1b-bf8a-1f3cfce1dcc0.png" alt="vendas_mes" title="vendas_mes" width="830" height="430" />
</p>

Um outro fator que se destaca é que o tipo de promoção interfere diretamente nas vendas, segundo os valores medidos na tabela.


<p align="center">
    <img src="https://user-images.githubusercontent.com/28810281/166600426-d1dba6a5-5d70-48bb-a63c-154dd9b38eb4.png" alt="vendas_mes" title="vendas_mes" width="180" height="180" />
</p>
 
E uma outra característica que influencia nas vendas é que a estrutura da loja como o seu assortment adotado e classificação que ela recebe. Isto é visto nas figuras abaixo.  
 
<p align="center">
    <img src="https://user-images.githubusercontent.com/28810281/166604230-6a7aa343-1d40-4044-83c5-516a979d2ea7.png" alt="vendas_mes" title="vendas_mes" width="430" height="430" />
     <img src="https://user-images.githubusercontent.com/28810281/166604232-0cdde400-9daf-4488-a3e8-c04d88c343a7.png" alt="vendas_mes" title="vendas_mes" width="430" height="430" />
</p>

### Desepeho dos modelos.
 
Entre os modelos testados aquele que apresentou o menor erro percentual é o Lightgbm, no caso o seu valor foi de  4.571 +/- 0.037 e com um bias de 182.365 +- 4.435. Para ambas medidas o intervalo de confiança utilizado é de 99%. Um ponto que se destaca sobre o desempenho dele é que a maioria do erro máximo percentual de diversas lojas não passam dos 20%. A quantidade das lojas que passaram desse valor é de 10%. 
 
 

 

 




 
 
 
 
 
 
 
 
 
