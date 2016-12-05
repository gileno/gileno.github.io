---
layout: post
title: Como analisar dados imobiliários com Python
slug: analise-de-dados-imobiliarios-com-python
date: 2016-08-11 22:00:00
author: Gileno Filho
category: tutoriais
tags: python,dados,engenharia-de-avaliacoes
---

Python tem sido cada vez mais utilizado como linguagem de programação dos cientistas de dados, juntamente com [R](https://www.r-project.org/). Desde 2009 eu trabalho junto com algumas pessoas da área de [Engenharia de Avaliações](https://pt.wikipedia.org/wiki/Engenharia_de_avalia%C3%A7%C3%B5es), o que despertou meu interesse pelo mercado imobiliário.

Eu já falei um pouco aqui no blog:

- [Técnicas de Regressão aplicadas a Avaliações de Bens com Python — Parte I](http://www.gilenofilho.com.br/tecnicas-de-regressao-aplicadas-a-avaliacoes-de-bens-com-python-parte-i/)
- [Técnicas de Regressão aplicadas a Avaliações de Bens com Python — Parte II](http://www.gilenofilho.com.br/tecnicas-de-regressao-aplicadas-a-avaliacoes-de-bens-com-python-parte-ii/)

Neste artigo eu irei mostrar a parte prática, como essa análise é feita e como podemos extrair informações para ajudar a entender o comportamento do mercado atual de uma determinada localidade. Abaixo segue o que iremos fazer:

- [Instalar e Configurar o ambiente Python](#ambiente)
- [Onde buscar dados imobiliários?](#captura)
- [Análise Exploratória](#exploracao)
- [Limpeza dos Dados](#limpeza)
- [Criação do Modelo de Regressão](#modelo)
- [Entendendo os resultados](#resultados)
- [Visualização e Comunicação](#visualizacao)

<div id="ambiente"></div>
### Instalar e Configurar o ambiente Python

Na área científica é comum que quem esteja por trás dos projetos sejam estatísticos, cientistas... e normalmente essas pessoas desejam utilizar as tecnologias de forma mais prática possível, isto é, se alguma ferramenta necessitar de um conhecimento muito avançado em computação pode dificultar o acesso e é por isso que [MATLAB](https://pt.wikipedia.org/wiki/MATLAB) e [R](https://www.r-project.org/) são fortes nesse ambiente. Essas ferramentas programáveis - são ao mesmo tempo uma linguagem e um ambiente científico - proporcionam um ambiente onde é possível manipular os dados, visualizar gráficos, codificar, salvar código e dados entre outras necessidades dessa área, tudo isso numa interface única de fácil instalação.

Para entender melhor o que eu falei veja essa palestra: [KTHXBAI, MATLAB: migrando a Academia para o Python](https://www.youtube.com/watch?v=mDk_uz3AKmY).

Pensando nisso a comunidade (pessoas, empresas e instituições) Python começaram a criar iniciativas que facilitem a entrada desses profissionais no mundo Python, porque Python se parece bastante com pseudo-códigos utilizados para explicar os algoritmos clássicos e tem uma sintaxe simples e objetiva. Numa dessas iniciativas surgiu o ipython que se tornou o [Jupyter](http://jupyter.org/) e a [Anaconda](https://docs.continuum.io/anaconda/). No tutorial irei utilizar o [miniconda](http://conda.pydata.org/miniconda.html) que é a versão mais simples da Anaconda, apenas com o Python e a ferramenta de gerenciar pacotes, após a instalação para criar um novo ambiente basta fazer assim (no terminal):

```
conda create -n dados-imobiliarios python=3
```

Dessa forma irei criar um ambiente Python 3 chamado *dados-imobiliarios* que pode ser ativado assim:

```
source activate dados-imobiliarios
```

Isso deve funcionar no Unix (Linux/Mac), no windows talvez tenha alguma diferença mas ainda sim é simples. Após ativar o ambiente - ativar serve para que o Python considerado seja o do ambiente e não alguma eventual instalação Python global - basta instalar algumas bibliotecas que iremos precisar:

```
conda install pandas statsmodels matplotlib seaborn jupyter
```

O legal de usar o *miniconda* é que é possível utilizar o comando *pip* também, caso a biblioteca não exista no repositório da [Continuum](http://repo.continuum.io/pkgs/) para o seu sistema operacional.

Agora basta utilizar o seu Editor de Texto favorito para Python ou utilizar a IDE [Spyder](https://pythonhosted.org/spyder/) que se integra bem com o miniconda.

<div id="captura"></div>
### Onde buscar dados imobiliários?

Normalmente no processo de análise de dados, nós tentamos extrair dos dados soluções para problemas feitos anteriormente. Isso é importante porque você consegue trazer foco para a análise e assim consegue utilizar as técnicas certas para cada problema que deseja resolver. Neste tutorial eu irei analisar dados imobiliários para avaliar apartamentos na cidade de Recife/PE.

Com base no propósito acima, eu preciso ter dados de outros apartamentos em Recife/PE para que analisando as características deles, com o valor o qual eles estão sendo ofertados, eu possa fazer algum tipo de comparação com os apartamentos que eu quero avaliar e gerar um valor aproximado da minha avaliação, também conhecido como **valor estimado de mercado**.

O ideal é ter algum tipo de conhecimento sobre os dados que se vai trabalhar, isso facilita a descoberta de anomalias. Eu sei que a localidade dos imóveis afeta o valor do metro quadrado, então eu não vou buscar imóveis que sejam de outras cidades ou regiões, pois é possível que as comparações não façam sentido ou deixe minha análise mais complexa a ponto de eu não conseguir estimar o valor dos imóveis com uma boa qualidade.

Uma fonte interessante de dados imobiliários são obtidos em sites de anúncios como o OLX, os valores geralmente oscilam muito mas é a fonte mais fácil. O ideal seria poder ter os valores reais das trasanções que foram efetuadas de compra e venda, mas para esse tutorial basta dados desses portais de imóveis. Se quiser automatizar o processo de captura de dados basta ver o tutoral que eu fiz com o Python/[Scrapy](http://scrapy.org/) no blog:

- [Usando o Scrapy e o Rethinkdb para capturar e armazenar dados imobiliários - Parte I](usando-o-scrapy-e-o-rethinkdb-para-capturar-e-armazenar-dados-imobiliarios-parte-i)
- [Usando o Scrapy e o Rethinkdb para capturar e armazenar dados imobiliários - Parte II](usando-o-scrapy-e-o-rethinkdb-para-capturar-e-armazenar-dados-imobiliarios-parte-ii)
- [Usando o Scrapy e o Rethinkdb para capturar e armazenar dados imobiliários - Parte III](usando-o-scrapy-e-o-rethinkdb-para-capturar-e-armazenar-dados-imobiliarios-parte-iii)

Eu já peguei alguns dados que estão disponíveis no repositório desse tutorial:

- [https://github.com/gileno/analise-dados-imobiliarios](https://github.com/gileno/analise-dados-imobiliarios)

<div id="exploracao"></div>
### Análise Exploratória

Com os dados em mãos iremos realizar uma análise exploratória
