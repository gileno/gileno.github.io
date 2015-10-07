---
title: "Usando o Scrapy e o Rethinkdb para capturar e armazenar dados imobiliários - Parte I"
layout: post
permalink: usando-o-scrapy-e-o-rethinkdb-para-capturar-e-armazenar-dados-imobiliarios-parte-i
date: 2015-06-25 14:23:00
author: Gileno Filho
categories: tutoriais
tags: python dados
---


### Introdução

Olá pessoal, a algum tempo que estou organizando minha agenda para voltar a trabalhar em alguns [Web Crawlers](https://pt.wikipedia.org/wiki/Web_crawler) para capturar dados imobiliários que é um tipo de dado que gosto de trabalhar. Assim resolvi publicar esse artigo, que fará parte de uma série de 3, onde irei mostrar como fazer um crawler usando o [Scrapy](http://scrapy.org/) e como armazenar num banco de dados que muito me interessa, o [rethinkdb](http://www.rethinkdb.com/).

### Agenda

- [Parte I - Configurando e rodando o Scrapy](http://gilenofilho.com.br/usando-o-scrapy-e-o-rethinkdb-para-capturar-e-armazenar-dados-imobiliarios-parte-i/)
- [Parte II - Instalando, configurando e armazenando os dados no Rethinkdb](http://gilenofilho.com.br/usando-o-scrapy-e-o-rethinkdb-para-capturar-e-armazenar-dados-imobiliarios-parte-ii/)
- [Parte III - Deploy do projeto Scrapy](http://gilenofilho.com.br/usando-o-scrapy-e-o-rethinkdb-para-capturar-e-armazenar-dados-imobiliarios-parte-iii/)

### Vamos lá

O Scrapy é um framework para facilitar o desenvolvimento de crawlers, pois mesmo sendo fácil fazer um crawler usando o built-in do Python como o [urllib](https://docs.python.org/2/library/urllib.html), ou bibliotecas externas como [requests](http://docs.python-requests.org/en/latest/), fica mais rápido e prático utilizar um conjunto de ferramentas desenhados para este fim, é o famoso "batteries included".

Para instalar o Scrapy vamos utilizar o pip (supondo que já esteja num [virtualenv](https://virtualenv.pypa.io/en/latest/)):

{% highlight sh %}
pip install scrapy
{% endhighlight %}

Após instalar o scrapy você terá disponível o comando "scrapy" mais detalhes sobre as opções dele aqui:

http://doc.scrapy.org/en/1.0/topics/commands.html

O scrapy é composto de "spiders" que é a parte do código que irá definir que páginas serão acessadas para capturar informações, "items" que são as informações que serão extraídas das páginas e os "pipelines" que irão definir como esses "items" serão processados.

Um exemplo simples de um crawler utilizando o Scrapy:

<script src="https://gist.github.com/gileno/8579ef62f5a700ca99d4.js"></script>

Para rodar basta utilizar o comando scrapy:

{% highlight sh %}
scrapy runspider gilenofilho.py
{% endhighlight %}

Você verá algo assim:

{% highlight sh %}
...
2015-06-22 18:26:07 [scrapy] DEBUG: Redirecting (301) to <GET http://gilenofilho.com.br/> from <GET http://www.gilenofilho.com.br/>
2015-06-22 18:26:07 [scrapy] DEBUG: Crawled (200) <GET http://gilenofilho.com.br/> (referer: None)
2015-06-22 18:26:07 [gilenofilho] DEBUG: Hello World: http://gilenofilho.com.br/
2015-06-22 18:26:07 [scrapy] INFO: Closing spider (finished)
2015-06-22 18:26:07 [scrapy] INFO: Dumping Scrapy stats:
...
{% endhighlight %}

Uma Spider é basicamente uma classe que herda de `scrapy.Spider` o atributo `start_urls` está definindo as urls que devem ser acessadas inicialmente, você pode definir um método `starts_requests` que deve retornar uma lista de `scrapy.Request` através da keyword `yield`, assim:

Obs: a implementação padrão do `starts_requests` procura o atributo `start_urls` e chama o método `parse`.

<script src="https://gist.github.com/gileno/83720a8c73a52685e399.js"></script>

Deve se utilizar `yield` e passar um **callback** para a `scrapy.Request` pois o scrapy faz requisições assíncronas, isto é, não espera a requisição inicial acabar para fazer uma nova requisição, e desta forma utiliza o conceito de geradores em Python, você pode ver mais detalhes de como geradores funcionam acessando as palestras de Luciano Ramalho em: http://pt.slideshare.net/ramalho/.

O scrapy tem o conceito de projeto onde ficam organizados as "Spiders", "items" e "pipelines". Para criar um projeto scrapy basta utilizar o comando:

{% highlight sh %}
scrapy startproject nome_do_projeto
{% endhighlight %}

Você verá que uma estrutura de diretórios e arquivos será criada para que facilite o crescimento do seu crawler. Eu criei um projeto chamado **scrapy_olx** e meu sistema de diretórios ficou assim:

{% highlight sh %}
scrapy_olx
- scrapy_olx
- - spiders
- - - __init__.py
- - __init__.py
- - items.py
- - pipelines.py
- - settings.py
- scrapy.cfg
{% endhighlight %}

Agora vamos criar nosso primeiro Spider, com o comando:

{% highlight sh %}
scrapy genspider olx pe.olx.com.br
{% endhighlight %}

Estou criando um crawler para capturar os imóveis de Pernambuco (PE) e esta é a url inicial no OLX. Dentro do diretório **spiders** foi criado um arquivo chamado olx.py contendo o esqueleto do nosso código, vou modificar o **starts_urls** para começar com a url dos imóveis para alugar, o arquivo modificado vai ficar assim:

<script src="https://gist.github.com/gileno/e533443087a86b4a5fb5.js"></script>

Para rodar este código basta utilizar o comando:

{% highlight sh %}
scrapy crawl olx
{% endhighlight %}

Se antes usamos a opção `runspider` agora que estamos num projeto scrapy usamos a opção `crawl` passando o nome da **spider**, no caso **olx**.

Agora vamos modificar o método `parse` para adicionar a lógica de verificar os links para os imóveis que a página contém, após isso iremos acessar a página do imóvel para só então capturar os dados do imóvel.

<script src="https://gist.github.com/gileno/b9013b0aa9b2d518fe6c.js"></script>

Agora no método parse usamos **xpath** para percorrer a estrutura do html e encontrar todos os **li** que contém a **class** css **item**, cada elemento deste tipo irá ter um imóvel e assim fazemos um for para buscar o **href** do link único para o imóvel. Ao pegar o link de cada imóvel retornamos através do **yield** uma nova requisição para o scrapy realizar e passamos desta vez outro callback, o `parse_detail`. Nesse primeiro momento ele apenas vai fazer o log da url.

Rodando novamente o código será possível que o scrapy irá realizar 51 requisições, 1 para cada imóvel - 50 por página - e a primeira para acessar a página inicial.

{% highlight sh %}
scrapy crawl olx
{% endhighlight %}

Após fazer a lógica de acessar cada imóvel vamos adicionar a parte de verificar se existe uma próxima página, visto que são exibidos 50 imóveis por página mas no final da página há uma paginação.

O código ficará assim:

<script src="https://gist.github.com/gileno/39d3d663a314a56c8e2b.js"></script>

Obs: Atualizei o código com a dica do [Elias Dorneles](https://twitter.com/eliasdorneles) sobre o **normalize-path**, essa função do **xpath** serve para remover o excesso de caracteres em branco e outros caracteres que a renderização do html ignora mas que está presente no código fonte.

Veja que após o `for` usamos novamente o xpath para encontrar o link que contém o texto **Próxima página** que está no final da página do OLX - basta examinar o html. Se houver o link mandamos outra requisição ao scrapy, só que desta vez o callback é o mesmo método que estamos, o `parse`. Para acrescentar fazemos o log do título do imóvel, dando uma ideia de como podemos pegar outras informações sobre o imóvel, mais detalhes sobre isso no próximo artigo.

Para rodar, basta novamente enviar o comando:

{% highlight sh %}
scrapy crawl olx
{% endhighlight %}

Para perceber que o scrapy é assíncrono nas suas requisições, basta ver que ele acessar a próxima página antes de acabar as requisições dos imóveis da primeira página.

Enfim, essa primeira parte fica por aqui, na próxima irei mostrar os conceitos de **Item** e **Pipeline** que o scrapy possui para capturar e processar os dados armazenados.

### Referências

- [Explorando Scrapy além do tutorial](https://speakerdeck.com/eliasdorneles/explorando-scrapy-alem-do-tutorial)
- [Documentação Oficinal do Scrapy](http://doc.scrapy.org/en/1.0/index.html)
