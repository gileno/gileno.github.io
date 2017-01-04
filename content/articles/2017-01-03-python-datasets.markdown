---
layout: post
title: Bibliotecas Python para carregar Dataset's
slug: python-datasets
date: 2017-01-02 09:00:00
author: Gileno Filho
category: tutoriais
tags: python,dados
ipython: true
---

Desde que a biblioteca [Pandas](http://pandas.pydata.org/) se tornou bastante popular em análise de dados com Python, várias outras libs surgiram para auxiliar a importação de dados para objetos do tipo DataFrame (utilizados pelo Pandas).

Neste artigo irei comentar sobre duas libs:

- [db.py](https://github.com/yhat/db.py): Facilita a importação de bancos de dados para DataFrame's
- [PyDataset](https://github.com/iamaziz/PyDataset): Prover uma forma simples de acessar diversos datasets públicos - dataset's disponibilizados por bibliotecas da linguagem R

## PyDataset

{% notebook notebooks/datasets-pydataset.ipynb %}

## db.py

O db.py faz conexão com os bancos relacionais mais utilizados, mas de acordo com o banco de dados será necessário instalar alguma biblioteca adicional, mais detalhes em:

- [https://github.com/yhat/db.py#installation](https://github.com/yhat/db.py#installation)

No exemplo abaixo irei utilizar o sqlite3, que é o único que não precisa de nenhuma instalação adicional porque a lib de comunicação já vem com a instalação Python. O arquivo do banco sqlite3 está aqui:

- [log database](/utils/logs.sqlite3)

{% notebook notebooks/datasets-db-py.ipynb %}

A db.py tem mais algumas opções, basta acessar o link acima e verá que é bem fácil fazer consultas que retornem DataFrame's do Pandas para realizar algum tipo de análise em memória.

Qualquer dúvida ou sugestão basta comentar abaixo!
