---
title: Usando o Scrapy e o Rethinkdb para capturar e armazenar dados imobiliários - Parte II
layout: post
slug: usando-o-scrapy-e-o-rethinkdb-para-capturar-e-armazenar-dados-imobiliarios-parte-ii
date: 2015-06-29 12:18:00
author: Gileno Filho
category: tutoriais
tags: python,dados
---

### Introdução

Olá pessoal, esta é a parte II da série sobre o Scrapy, abaixo os links para todos os artigos da série:

- [Parte I - Configurando e rodando o Scrapy](http://gilenofilho.com.br/usando-o-scrapy-e-o-rethinkdb-para-capturar-e-armazenar-dados-imobiliarios-parte-i/)
- [Parte II - Instalando, configurando e armazenando os dados no Rethinkdb](http://gilenofilho.com.br/usando-o-scrapy-e-o-rethinkdb-para-capturar-e-armazenar-dados-imobiliarios-parte-ii/)
- [Parte III - Deploy do projeto Scrapy](http://gilenofilho.com.br/usando-o-scrapy-e-o-rethinkdb-para-capturar-e-armazenar-dados-imobiliarios-parte-iii/)

Na parte I mostrei como instalar/configurar e rodar seu projeto scrapy no site do OLX. Nesse artigo vamos ver como salvar as informações resgatadas do crawler.

Antes de ir ao código é importante frisar que o Scrapy sempre que recebe um `scrapy.Request` dentro de uma **callback** irá realizar outra requisição, entretanto se ao invés disso, você retornar um dicionário ou um objeto que herde de `scrapy.Item`, o Scrapy irá entender que aquele **callback** acaba de resgatar uma informação que deve ser processada e vai enviar esse item ou dicionário para a fila de processamento - os **pipelines**.

### Vamos lá

Dentro do **callback** que definimos no último [código da parte I](https://gist.github.com/gileno/39d3d663a314a56c8e2b#file-olx-py), nós vimos como pegar uma informação da requisição via **xpath** e exibir essa informação no nosso log, agora vamos fazer a lógica de informar ao Scrapy que dados estamos coletando e por fim vamos criar um **pipeline** para processar esses dados.

O código ficará assim:

<script src="https://gist.github.com/gileno/6fbc0cbf1fed942b85de.js"></script>

A grande mudança é que agora nós estamos coletando bem mais informações sobre o imóvel, ainda da forma **crua** mas limpeza desses dados ficaria para um possível tratamento estatístico... Estamos criando um dicionário chamado `item` e no final usamos o `yield` para retorná-lo. A primeira informação que está sendo guardada são as fotos, quer dizer, os links para as fotos, utilizando o `extract()` ou invés do `extract_first()` pois provavelmente irá retornar mais de um elemento no **xpath** da fotos.

Todas as outras informações são simples de coletar, basta um pequeno **xpath** utilizando a função **normalize-space** para remover caracteres indesejados como **\t*** a única informação que necessita de algo diferente é a data, ela não está num formato interessante mas conseguimos pegar ao menos o dia, mês e hora utilizando a expressão regular presente na linha [55](https://gist.github.com/gileno/6fbc0cbf1fed942b85de#file-olx-py-L55). Como não tenho certeza se todos os imóveis irão cair nessa regex, faço uma pequena verificação se a regex obteve êxito.

Agora que estamos retornando nossas informações basta rodar novamente o crawler:

```
scrapy crawl olx
```

Devemos ver algo assim:

```
...
2015-06-28 21:49:38 [scrapy] DEBUG: Scraped from <200 http://pe.olx.com.br/grande-recife/imoveis/apto-kitnet-c-2-qtos-j-piedade-p-casal-s-filhos-ou-solteiros-95174559>
{'date': u'28 Junho 19:10', 'title': u'Apto Kitnet c/2 qtos, J.Piedade p/casal s/filhos ou solteiros', 'url': 'http://pe.olx.com.br/grande-recife/imoveis/apto-kitnet-c-2-qtos-j-piedade-p-casal-s-filhos-ou-solteiros-95174559', 'price': u'R$500', 'photos': [u'http://img.olx.com.br/images/14/145528016191488.jpg', u'http://img.olx.com.br/images/14/147528011762579.jpg', u'http://img.olx.com.br/images/14/141528016763146.jpg', u'http://img.olx.com.br/images/14/149528019791781.jpg'], 'details': u'Local adequado para quem gosta de tranquilidade e sil\xeancio, apto com 2 qtos, bem conservado, todo na cer\xe2mica, ideal para casal ou para solteiros SEM FILHOS E SEM ANIMAIS DE ESTIMA\xc7\xc3O. N\xc3O TEM GARAGEM PARA CARROS E NEM LUGAR PARA COLOCAR NA FRENTE, dispomos apenas de vagas para motos, contadores de luz individuais, banheiro com box, ambiente familiar, n\xe3o adequado para quem gosta de briga, som alto e bebedeira. Local tranquilo, rua sem asfalto, condom\xednio fechado e muito organizado perto de com\xe9rcio, transporte, etc. Fica em Jardim Piedade Pr\xf3ximo ao supermercado todo dia, na Rua do Sossego N\xba 100 CEP 54420680. Valor do aluguel R$ 500,00 com \xe1gua inclusa. N\xe3o exigimos fiador, contrato m\xednimo de 6 meses. Falar com \xc2ngela pelo n\xfamero 81-97961646 tim e 88226083 oi. Mais fotos do interior do apto via Whatzapp.', 'address': u'Localiza\xe7\xe3o Munic\xedpio: Jaboat\xe3o dos Guararapes Bairro: Piedade CEP do im\xf3vel: 54410-695', 'source_id': u'95174559'}
2015-06-28 21:49:39 [scrapy] DEBUG: Crawled (544) <GET http://pe.olx.com.br/grande-recife/imoveis/apto-no-10-andar-em-quase-beira-mar-03qtos-95175476> (referer: http://pe.olx.com.br/imoveis/aluguel)
...
```

Por padrão o Scrapy irá apenas logar a informação coletada, vamos agora implementar um pipeline para armazenar a informação no banco da dados [rethinkdb](http://www.rethinkdb.com/). Eu resolvi utilizar o rethinkdb porque gosto de experimentar novos bancos de dados e ele tem diversos aspectos interessantes do NoSQL e algumas facilidades dos bancos relacionais clássicos, em outro artigo eu entro em mais detalhes sobre esse banco de dados - qualquer coisa basta citar essa escolha nos comentários - por hora basta saber que ele armazena documentos no formato JSON.

Primeiro precisamos baixar e instalar, algo que é bem simples, basta acessar o site oficial e escolher o pacote para o seu sistema operacional:

http://www.rethinkdb.com/docs/install/

Após a instalação é preciso colocar o rethinkdb para rodar, basta digitar o comando:

```
rethinkdb
```

Com o banco de dados rodando você tem acesso a uma interface administrativa acessando:

http://localhost:8080/

Eu prefiro colocar o banco de dados parar rodar só quando vou utilizar, faço isso tanto com os relacionais quanto os não-relacionais mas se desejar pode iniciar o rethinkdb assim que iniciar o sistema:

http://rethinkdb.com/docs/start-on-startup/

Com o banco de dados rodando, devemos acessar a interface administrativa e criar um banco de dados chamado **scrapy_olx**. Depois de criado o banco, vamos instalar o driver do rethinkdb:

```
pip install rethinkdb
```

Agora vamos adicionar às configurações do nosso projeto Scrapy, arquivo **settings.py**, as informações de acesso ao rethinkdb e a configuração `ITEM_PIPELINES` indicando o pipeline que iremos criar.

{% highlight python %}
RETHINKDB = {
    'table_name': 'items', 'db': 'scrapy_olx'
}
ITEM_PIPELINES = {
    'scrapy_olx.pipelines.RethinkdbPipeline': 1
}
```

Com as configurações inseridas no **settings.py** vamos alterar o arquivo pipelines.py para adicionar a classe `RethinkdbPipeline`, que irá processar nossos dados e inserir no rethinkdb:

<script src="https://gist.github.com/gileno/3219ab7caf5be6da5478.js"></script>

A primeira coisa que fazemos é importar o módulo do rethinkdb, eles recomendam usar o namespace **r** mas é opcional.

{% highlight python %}
import rethinkdb as r
```

Cada classe que irá ser um [pipeline](http://doc.scrapy.org/en/1.0/topics/item-pipeline.html#item-pipeline) pode implementar 4 métodos:

- [process_item](http://doc.scrapy.org/en/1.0/topics/item-pipeline.html#process_item)
- [open_spider](http://doc.scrapy.org/en/1.0/topics/item-pipeline.html#open_spider)
- [close_spider](http://doc.scrapy.org/en/1.0/topics/item-pipeline.html#close_spider)
- [from_crawler](http://doc.scrapy.org/en/1.0/topics/item-pipeline.html#from_crawler)

No método `from_crawler` nós temos acesso a todos os principais componentes do Scrapy, incluindo as configurações e por isso implementamos este método para pegar as informações de acesso ao rethinkdb.

Nos método `open_spider` e `close_spider` fazemos a abertura e fechamento da conexão com o rethinkdb, para evitar erros há uma pequena verificação se a tabela já existe no banco de dados, caso não exista ela é criada.

Finalmente no método `process_item` inserimos o item no banco de dados, o rethinkdb aceita dicionários que tem uma estrutura semelhante aos JSON's que é a forma de armazenamento dele.

Agora vamos rodar novamente o crawler:

```
scrapy crawl olx
```

O crawler deve rodar durante algumas horas mas ao acessar a interface administrativa do rethinkdb irá perceber que o número de documentos indicados na tabela **items** vai aumentando.

### Resumo

Neste artigos vimos como retornar ao Scrapy as informações coletadas, depois tivemos uma visão geral do rethinkdb um banco conhecido como **scalable JSON database**, ele é open-source e construído para aplicações web em tempo real.

Por fim fizemos um pipeline para ver como podemos processar um item coletado pelo crawler, utilizamos todos os 4 métodos que podem ser implementados pelo pipeline e são chamados pelo Scrapy.

No próximo artigo iremos ver como fazer deploy do projeto Scrapy, pois normalmente não é interessante deixar o crawler rodando na sua máquina, o mais comum é colocar em algum servidor na nuvem.
