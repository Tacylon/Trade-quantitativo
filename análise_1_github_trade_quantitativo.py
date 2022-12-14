# -*- coding: utf-8 -*-
"""Análise 1 github - Trade Quantitativo.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LTlaE1d3iMK1lliZem2E-ue5ETWeVug4

# Setup
"""

## Run This Cell for Colab
!pip install yfinance
!pip install vectorbt
!pip install quantstats



import vectorbt as vbt
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

"""## Definindo parâmetros"""

# Análise de um Ativo Americano
codigo = 'BTC-USD'
ativos_comparacao = [codigo, 'ETH-USD', 'ADA-USD']

data_inicial = '2018-01-01'  
data_final = '2019-01-01'

# Os preços de fechamentos dos ativos
vbt.YFData.download(ativos_comparacao, start=data_inicial, end=data_final).get('Close')

"""## Baixando os dados"""

precos = vbt.YFData.download(codigo, start=data_inicial, end=data_final).get()
fechamento = vbt.YFData.download(codigo, start=data_inicial, end=data_final).get('Close')

"""# Analisando a Série"""

fechamento.vbt.plot().show()

precos.vbt.ohlcv.plot().show()

"""## Gráfico comparativo

Com investimento inicial de \$1 (ou R\$ 1)
"""

vbt.YFData.download(ativos_comparacao,
                    start=data_inicial,
                    end=data_final).plot(column='Close', base=1).show()

"""## Gráfico Quant Stat

Retorno Cumulativo, Drawdown e Retorno Diário
"""

warnings.filterwarnings('ignore')

retornos = fechamento.vbt.to_returns()
retornos.vbt.returns.qs.plot_snapshot(title=codigo)

"""# Analisando Estratégias de Trade

## Simple Moving Averages
"""

n_periodos_curta = 21
n_periodos_longa = 50

media_curta = vbt.MA.run(fechamento, n_periodos_curta, short_name='media_curta')
media_longa = vbt.MA.run(fechamento, n_periodos_longa, short_name='media_longa')

fig = fechamento.vbt.plot(trace_kwargs=dict(name='Preço de Fechamento'))
media_curta.ma.vbt.plot(trace_kwargs=dict(name='Média Móvel Curta'), fig=fig)
media_longa.ma.vbt.plot(trace_kwargs=dict(name='Média Móvel Longa'), fig=fig)

fig.show()

"""A média móvel inclinada para cima sinaliza uma tendência de alta. Média móvel inclinada para baixo sinaliza uma tendência de baixa do preço. Podemos observar que quando o grafico transpassa a média móvel curta, o grafico tende a ir pelo lado oposto do grafico, indicando uma oportunidade de compra/venda. Ex.(Feb 14, 2018, quando o grafico passou pela média móvel curta o grafico fez a tendencia de alta, aonde seria nosso ponto ideal para comprar, quando fez o mesmo processo no em Mar 7, 2018, a média móvel curta ia fazendo o movimento de alta e o grafico o movimento de baixa, nesse ponto seria o ideal para o movimento de venda. 
Quando inserimos a média móvel longa ao cruzar com a média móvel curta, temos a probabilidade da analise está mais acertiva.

## Relative Strength Index
"""

rsi = vbt.RSI.run(fechamento)
rsi.plot().show()

"""- O Indicador RSI funciona por meio da elaboração de um comparativo entre as perdas e os ganhos em um determinado período, utilizando uma média de cada um desses fatores para fazer os cálculos. Para compreender o que o número resultante das contas, é preciso levar em consideração que, nesse índice, cada faixa de valores entre 0 a 100 corresponde a indicativos diferentes sobre esse ativo. São eles:
 - 0 a 30: significa que há uma situação de sobrevenda. 
 - entre 30 e 70: há uma espécie de equilíbrio nesse momento. 
 - 70 a 100: o mercado está caminhando para a supercompra. 
- No grafico acima podemos observar que teve bastante movimentação (impulso) do ativo, as mudanças no RSI junto com as mudanças no gráfico de preços podem ser um poderoso indicador de reversões de tendência. No entanto não e possivel analisar exatamente quando essas reversôes acorrerão.

## Stochastics

The TA-Lib Stoch function returns two lines slowk and slowd which can then be used to generate the buy/sell indicators.
A crossover signal occurs when the two lines cross in the overbought region (commonly above 80) or oversold region (commonly below 20).
When a slowk line crosses below the slowd line in the overbought region it is considered a sell indicator.
Conversely, when an increasing slowk line crosses above the slowd line in the oversold region it is considered a buy indicator.
"""

vbt.STOCH.run(precos['High'], precos['Low'], precos['Close']).plot().show()

"""- A linha K é a linha mais “rápida”, e é calculada pela divisão entre a diferença do preço do fechamento e a menor mínima do período.
- A curva D, é a linha mais “lenta”, e é representada pela mediana móvel simples de 3 dias da linha K.

O cruzamento da linha rápida (%K) com a linha mais suave (%D) pode gerar sinais de entrada e saída, por exemplo. Se a linha K cruzar acima da linha D, há um indício de compra bem favorável. Se o contrário acontecer, podemos estar diante de um sinal de venda.

## Bollinger Bands
"""

vbt.BBANDS.run(fechamento).plot().show()

"""A principal função das Bandas de Bollinger é tentar prever como um ativo vai se comportar no seu movimento de preço. Para isso são determinados o preço médio, mínimo e máxima de um período. De forma simples, as bandas criam uma “área” onde é possível tentar determinar se o preço vai sofrer uma valorização ou uma queda, baseado no histórico deste ativo em um determinado período.

A partir das linhas, há como pintar um possível cenário para tentar determinar se o ativo está em um momento de sobre-compra ou sobre-venda. Destacando que as bandas não devem ser utilizadas como única métrica e é necessário utilizar outras ferramentas. quando o ativo bate na linha superior, e um bom indicativo de venda, quando o grafico bate na linha inferior e um bom indicativo de comprar o ativo. 
"""