
### :pushpin: [__Read in English__](https://github.com/pedropscf/1-Rossman-Sales-Prediction/blob/9f5a47b70bb4d2f06bd1a78f84ba686b570431f4/README-en.md)

# Previsão de vendas nas lojas da Rossman ao longo das próximas 6 semanas

A Rossman é uma empresa do farmacêutico e contém mais de 3000 lojas espalhadas ao longo de 7 países diferentes da Europa. A empresa apresentou um desafio na plataforma Kaggle relacionado à dificuldade que a empresa possui em realizar previsões de vendas. Isso ocorre devido ao fato de que há milhares de gerentes locais que possuem metodologias próprias de previsão. Além disso, há outros fatores que podem não estar sendo utilizados nas previsões destes gerentes, como inflluência de feriados e sazonalidade.

Com isso, a empresa precisa de uma solução que seja capaz de prever as vendas ao longo das próximas 6 semanas de cada uma das lojas. Portanto, a principal pergunta para o problema é:

- **Qual será o total de vendas realizado pela loja X ao longo das próximas 6 semanas?**

## Features

Para responder ao desafio levantado pela empresa, ela disponibilizou um conjunto de dados contendo vendas diárias em cada uma das lojas, além de informações acerca do tipo de loja, variedade de produtos e se a loja apresenta uma promoção ativa na data. De forma geral, as features no conjunto de dados foram:

| Feature  | Descrição |
| ------------- | ------------- |
| store  | Número da loja |
| day_of_week  | Dia da semana  |
| date  | Data das vendas  |
| sales | Valor total vendido pela loja na data |
| customers | Número de clientes que passaram pela loja |
| open | Se a loja estava aberta na data |
| promo | Se a loja apresenta promoções |
| state_holiday | Feriados nacionais |
| school_holiday | Feriados escolares |
| store_type | Tipo da loja |
| assortment | Variedade de produtos disponíveis |

Além das features anteriores, há ainda features relacionadas a distância e idade de competidores próximos e sobre promoções estendidas.

## Solução

O problema foi classificado como um problema clássico de regressão usando aprendizado de máquina em séries temporais. A solução foi realizada em ciclos de desenvolvimento de ponta a ponta e pode ser descrita resumidamente (a solução completa junto com os códigos desenvolvidos pode ser vista [aqui.](https://github.com/pedropscf/1-Rossman-Sales-Prediction/blob/7e3111cdad78d7373659ab99296c9290d8afb02d/m05_vid01_store_sales_prediction_PTBR.ipynb)) em:

### Limpeza e manipulação dos dados

O conjunto de dados contém mais de 1 milhão de linhas e 18 colunas e o trabalho inicialmente realizado foi para a adequação dos tipos de dados no dataframe, seguido pelo tratamento dos valores nulos existentes para as features relacionados aos competidores e promoções estendidas.

### Feature Engineering

Aqui, as principais features criadas foram derivadas da data, como o número da semana no ano, o mês e o ano. Devido ao alto número de valores nulos para os atributos de promoções estendidas, foram criadas features mesclando informações sobre promoções e promoções estendidas.

### Análise Exploratória de Dados (EDA)

Na análise exploratória de dados foi realizada uma análise para a distribuição de cada uma das variáveis, as relações entre variáveis a partir de uma análise bivariada, matriz de correlações entre variáveis numéricas e correlações entre variáveis categóricas. Também foram realizadas análises acerca do comportamento da variável resposta (sales) para as diferentes variáveis categóricas, como tipo de loja e variedade de produtos.

Por fim, foram levantadas uma śerie de afirmações acerca do que se espera para as vendas de uma loja e algumas delas foram testadas, ajudando a trazer insights para a modelagem do problema.

### Seleção de features e transformação

Inicialmente, todas as features sofreram algum tipo de transformação:

- Logarítmica: a feature alvo, sales, sofreu transformação logarítimica com o objetivo de tornar a curva mais próxima de uma curva normal.
- Rescala: outras features foram aplicados os métodos de RobustScaler e MinMaxScaler, como o ano e a distância até o competidor.
- Natureza: features mais relacionadas à data, como o número da semana, mês-ano, sofreu uma transformação de natureza ao serem divididas em uma parcela cosseno e outra parcela seno, com o objetivo de manter a ideia de ciclicidade destas variáveis
- Normalização: nenhuma feature foi normalizada.

Com todas as features devidamente transformadas e rescaladas, utilizou-se um regressor de Random Forest e o algoritmo Boruta sobre os dados com o objetivo de extrair informações acerca de quais são as features ou combinações delas que mais trazem informação à tarefa de regressão. Com isso, é possível decidir quais features seguirão para o treinamento e quais serão removidas.

### Treinamento dos modelos e validação cruzada ao longo do tempo

A partir das features selecionadas foram treinados diferentes modelos de regressores sobre os dados, como regressão linear, regressão linear regulzarizada, random forest regressor e o XGBoost. Inicialmente, foi realizado um treinamento sobre todos os dados de treinamento, seguindo pela avaliação dos modelos com o conjunto de testes, salvando-se métricas de erro como: erro médio absoluto percentual e erro médio quadrático. Em seguida, foi realizado um treinamento dos modelos em uma valização cruzada ao longo do tempo, dividido em 5 intervalos. As métricas de erro para cada intervalo foram salvas.

Com isso, observou-se que os modelos baseados em regressão linear apresentavam erros muitos altos, da ordem de um modelo simples de média, indicando que estes modelos não estariam ou aprendendo os dados, ou seriam incapazes de capturar bem o fenômeno. O que faz sentido, uma vez que foram observadas relações não lineares entre diferentes variáveis. Os modelos de Random Forest ou XGBoost apresentam métricas muito melhores, sendo o modelo escolhido o XGBoost.

### Análise da performance do modelo

Finalmente, com o modelo treinado, tunado, pode-se responder à pergunta levantada pela empresa:

- **Qual será o total de vendas realizado pela loja X ao longo das próximas 6 semanas?** O modelo foi colocado em produção a partir do ambiente de Cloud do Heroku, além da criação de um bot do Telegram que é capaz de responder a pergunta para cada uma das lojas disponíveis para o treinamento. O robô pode ser acessado a partir [deste canal do Telegram](https://t.me/pedropscf_RossmanBot). Com isso, é possível consultar, a qualquer momento, a previsão de vendas de cada uma das lojas  através de uma metodologia única.

- Outros pontos a serem observados, considerando a métrica do erro percentual médio absoluto, é possível obter valores para um range estimado para a previsão de vendas para o próximo período (neste caso, 6 semanas). Com isso, o **valor previsto de vendas para todas as lojas foi de aproximadamente $279 milhões**, com o pior cenário de vendas para $240 milhões e o melhor cenário de vendas aproximadamente a $317 milhões.

<p align="center">
  <img src="https://github.com/pedropscf/1-Rossman-Sales-Prediction/blob/7e3111cdad78d7373659ab99296c9290d8afb02d/img/model_results.png" />
</p>

- Ao observar os resultados do modelo e previsão e seus respectivos erros, observa-se que o modelo apresenta uma pequena tendência em prever valores de vendas menores que o realizado (conforme verifica-se o skewness do erro tendendo para o lado negativo), dessa forma há um certo nível de conservadorismo pelas respostas apresentadas.

## Ferramentas utilizadas

**Data manipulation and cleaning:** pandas, numpy

**Data visualization:** matplotlib, seaborn

**Machine learning:** Regressão (scikit-learn e xgboost), selação de features (Boruta)

**Ambiente Cloud:** Flask, requests, desenho de API e Heroku


## Sobre mim
Entusiasta de ciência de dados, aprendendo sobre aplicações de Machine Learning, IA e Ciência de dados em geral para a solução de diversos problemas de negócios.

## Autor

- Pedro Fernandes [@pedropscf](https://www.github.com/pedropscf)

