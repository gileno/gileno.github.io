---
title: "Técnicas de Regressão aplicadas a Avaliações de Bens com Python — Parte II"
layout: post
permalink: tecnicas-de-regressao-aplicadas-a-avaliacoes-de-bens-com-python-parte-ii
date: 2014-10-24 17:49:00
author: Gileno Filho
categories: tutoriais
tags: python engenharia-de-avaliações
---

Parte I - http://gilenofilho.com.br/tecnicas-de-regressao-aplicadas-a-avaliacoes-de-bens-com-python-parte-i/

## Introdução

Na primeira parte desta série eu escrevi de forma bem simples sobre o que seria a regressão linear mútipla e a Engenharia de Avaliações. Fui bem objetivo pois este assunto é bastante longo e eu achei melhor deixar algumas referências caso tenham interesse em se aprofundar.

Nesta segunda parte irei mostrar como funciona a avaliação de bens no Brasil. Ela é regida por normas técnicas da ABNT (Associação Brasileira de Normas Técnicas), essas normas são criadas por comissões de estudo formadas por produtores, consumidores e neutros (laboratórios, universidades e outros). No caso das normas para avaliação de imóveis que é a área que tenho mais interesse, elas foram construídas por uma comissão de estudo da construção civil, abaixo seguem as normas da área:

- [NBR 14653-1: Avaliação de Bens - Procedimentos Gerais 2010](https://dl.dropboxusercontent.com/u/9069443/NBR_14653-1_Norma_de_Avaliacoes_de_Bens_-_Procedimentos_Gerais.pdf)
- [NBR 14.653-2: Avaliação de Imóveis Urbanos 2010](https://dl.dropboxusercontent.com/u/9069443/NBR_14.653-2_Imoveis_Urbanos_Revisada_2010.pdf)
- [NBR 14653-3: Avaliação de Imóveis Rurais 2010](https://dl.dropboxusercontent.com/u/9069443/NBR_14653-3_Avaliacao_de_Imoveis_Rurais_1.pdf)

Os principais métodos aprovados pela normal são os seguintes:

### Método comparativo direto de dados de mercado

É o método que identifica o valor de um bem através do tratamento técnico dos atributos que o constitui comparando-os com uma determinada amostra, isto é, o bem é avaliado com base na comparação direta de seus atributos com os atributos de uma amostra a qual têm já definido os seus valores. Na [parte I](http://gilenofilho.com.br/tecnicas-de-regressao-aplicadas-a-avaliacoes-de-bens-com-python-parte-i/) quando eu mostrei a regressão linear, eu estava demonstrando o uso do método comparativo.

A norma permite outras formas de avaliação utilizando-se de dados do mercado, por exemplo, é possível utilizar uma rede neural. Além de disso a norma também explica detalhes técnico-científicos para que uma avaliação seja qualificada, isto é, existe uma formalidade metodológica para a avaliação.

### Método Involutivo

Este método identifica o valor do bem com base num estudo de viabilidade técnico-econômico considerando o seu aproveitamento eficiente. Um exemplo seria uma avaliação de uma [Gleba](http://legislacao.planalto.gov.br/legisla/legislacao.nsf/8b6939f8b38f377a03256ca200686171/a05d1c9a21be8cc603256a1f0044905a?OpenDocument), onde o método considera os custos de urbanização, impostos, lucro entre outros fatores para a criação de um empreendimento, no caso a venda de lotes. No fim, é possível chegar ao valor da Gleba e assim a avaliação.

### Método Evolutivo

O método evolutivo trabalha em cima do somatório dos componentes do bem a ser avaliado, para o caso de obter o valor de mercado se faz necessário adicionar um fator de comercialização que irá multiplicar o somatório. O somatório seria o valor de reedição ou custo de reprodução do bem nos dias atuais, isto é, considerando fatores de depreciação por exemplo.

## Onde entra Python?

Esta parte II ficou apenas na teoria, foi uma breve (**muito breve**) conversa sobre Engenharia de Avaliações. Na verdade eu deveria ter começado com essa parte teórica mas como meus pensamentos são turvos comecei do meio e voltei ao início. Nas próximas partes irei detalhar cada método e implementá-lo em Python, mas o foco será o método comparativo de mercado, pois como o título do artigo diz, a ideia é ver técnicas de regressão.
