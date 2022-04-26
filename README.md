# Forecast-stores 
 
### Descrição.
 
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
 
### Objetivo.
 
Sendo assim, esse trabalho visa realizar a predição de vendas dessas lojas através de um modelo de machine learning e a criação de um api que retorne as previsões feitas por ele.  
 
 
### Metodologia
 
Este projeto será baseado no processo padrão Cross-industry para mineração de dados (CRISP-DM). Uma ideia padrão sobre projeto de ciência de dados pode ser linear: preparação de dados, modelagem, avaliação e implantação. No entanto, quando usamos a metodologia CRISP-DM, um projeto de ciência de dados se torna uma forma circular. Mesmo quando termina em Deployment, o projeto pode ser reiniciado novamente pela Business Understanding. Como isso pode ajudar?
 
 
<p align="center">
    <img src="https://upload.wikimedia.org/wikipedia/commons/b/b9/CRISP-DM_Process_Diagram.png" alt="Kitten" title="A cute kitten" width="430" height="430" />
</p>
 
Pode ajudar a evitar que o cientista de dados pare em uma etapa específica e perca tempo com ela. Quando todo o projeto estiver concluído, o cientista de dados pode retornar à etapa inicial e fazer todas as etapas novamente. Portanto, o objetivo principal é seguir círculos conforme a necessidade. 
 
### Pipeline
 
* Tratamento dos dados.
* Análise dos dados.
* Preparação dos dados.
* Feature Engineering.
* Modelagem dos modelos de Machine Learning.
* Ajuste dos hiperparâmetros.
* Avaliação do melhor modelo. 
* Deploy do modelo (Construção).
 
### Aquisição dos dados.
 
Esse conjunto de dados foi originalmente usado em uma competição da Kaggle e foi fornecido com dados históricos de vendas de 1.115 lojas Rossmann. 
 
### Descrição das partes do projeto
 
Essa primeira parte do projeto está encarregada de tratar os dados, avaliá-los e criar o modelo de machine learning. Esse estudo foi dividido nas seguintes partes:
* Tratamento dos dados: Nesta parte foi realizado o tratamento dos dados faltantes, outliers e unir os conjuntos Train e Test.Também serão criadas algumas variáveis para dar suporte nas análises que serão feitas.
* Descrição dos dados: É visto como as vendas se relacionam com o tempo e qual é a relação de cada variável com os dados de Target.
* Parte 1 Modification dataset : Nesta parte será encontrado a melhor maneira de representar as variáveis discretas e selecionar as melhores variáveis para treinar o modelo.
* Parte 2 Modification dataset : Continuação do notebook Parte 1 Modification dataset.
 
**Todas essas partes se encontram na pasta chamada Notebooks**
  
 
**A segunda parte do projeto é o deploy do modelo, só que ela está em construção.**
 
 
 
 
 
 
 
 
 
 
