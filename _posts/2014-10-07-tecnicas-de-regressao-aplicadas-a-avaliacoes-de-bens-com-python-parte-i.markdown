---
title: "Técnicas de Regressão aplicadas a Avaliações de Bens com Python — Parte I"
layout: post
permalink: tecnicas-de-regressao-aplicadas-a-avaliacoes-de-bens-com-python-parte-i
date: 2014-10-07 11:24:00
author: Gileno Filho
categories: tutoriais
tags: python engenharia-de-avaliações
---

***O que são modelos de regressão e como usá-los na avaliação de bens em geral usando Python.***

Esse é um post migrado do Medium.

### Introdução

Na estatística, a [Regressão](http://pt.wikipedia.org/wiki/Regress%C3%A3o) é um meio de inferir o valor de uma dada variável dependente com base em variáveis independentes, também chamadas de variáveis explicativas. Em outras palavras, a ideia é gerar um modelo que possa explicar o comportamento de determinado conjunto de dados, em perspectiva de uma variável, na avaliação de bens, a variável tende a ser o preço do bem a ser avaliado.

A [Engenharia de Avaliação](http://pt.wikipedia.org/wiki/Engenharia_de_avalia%C3%A7%C3%B5es) é o ramo da engenharia que se concentra em estudar as diversas formas de se gerar o valor de um bem — avaliação do bem — e em geral é associada a avaliação imobiliária mas pode ser usada para avaliar outros bens como: máquinas, empresas, veículos…

Existem modelos de regressão que usam inferência estatística e outros que usam técnicas de inteligência artificial — como uma rede neural que pode ser usada tanto para classificação como para regressão. Nesta primeira parte irei mostrar o modelo clássico de regressão linear múltipla[1][2] — usando o método dos mínimos quadrados[3] — uma técnica estatística que visa gerar um modelo matemático — função linear — que será usada para inferir o valor da variável dependente com base nas variáveis independentes, o final o modelo fica assim:

![Equação do Modelo de Regressão](/content/images/2014/10/regression-multiple.png)

No modelo, o Y chapéu é a variável dependente, os X's são as variáveis independentes, o beta zero é o intercepto e os outros beta's são os parâmetros gerados pelo modelo que indica o declive da reta de regressão em relação a variável que ele está associado.

O método dos mínimos quadrados (MMQ) ou Ordinary Least Squares (OLS), é uma otimização matemática que visa minimizar a soma do quadrado dos erros, aproximando a equação linear para o conjunto de dados [3] — este link da wikipédia explica em detalhes como é feito essa regressão. Está é uma versão geral, para mais detalhes olhar as referências.

### Regressão Linear em Python

Em python temos algumas bibliotecas que já fazem a regressão linear:

http://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.linregress.html

http://pysal.readthedocs.org/en/v1.7/library/spreg/ols.html

Marcel Caraciolo fez um artigo em inglês muito bom fazendo uma implementação em Python, vale a pena conferir: http://aimotion.blogspot.com.br/2011/10/machine-learning-with-python-linear.html

Uma simples implementação de regressão usando a biblioteca científica [numpy](http://www.numpy.org/) — apenas para uso didático:

https://gist.github.com/gileno/1b58b43e7b1d13eabfaa

### Referências

[1] DANTAS, Rubens Alves. Engenharia de Avaliações — Uma Introdução à Metodologia Científica. 1ª Edição, Editora Pini, 1998

[2] http://pt.wikipedia.org/wiki/Regress%C3%A3o_linear

[3] http://pt.wikipedia.org/wiki/M%C3%A9todo_dos_m%C3%ADnimos_quadrados
