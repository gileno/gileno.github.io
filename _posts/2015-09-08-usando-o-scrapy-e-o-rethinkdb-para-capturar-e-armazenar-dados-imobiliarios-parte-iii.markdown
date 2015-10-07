---
title: Usando o Scrapy e o Rethinkdb para capturar e armazenar dados imobiliários - Parte III
date: 2015-09-08 13:33:00
permalink: usando-o-scrapy-e-o-rethinkdb-para-capturar-e-armazenar-dados-imobiliarios-parte-iii
author: Gileno Filho
layout: post
categories: tutoriais
tags: python dados
---

### Introdução

Olá pessoal, esta é a parte III da série sobre o Scrapy, abaixo os links para todos os artigos da série:

- [Parte I - Configurando e rodando o Scrapy](http://gilenofilho.com.br/usando-o-scrapy-e-o-rethinkdb-para-capturar-e-armazenar-dados-imobiliarios-parte-i/)
- [Parte II - Instalando, configurando e armazenando os dados no Rethinkdb](http://gilenofilho.com.br/usando-o-scrapy-e-o-rethinkdb-para-capturar-e-armazenar-dados-imobiliarios-parte-ii/)
- [Parte III - Deploy do projeto Scrapy](http://gilenofilho.com.br/usando-o-scrapy-e-o-rethinkdb-para-capturar-e-armazenar-dados-imobiliarios-parte-iii/)

Nos artigos anteriores mostrei como capturar os dados imobiliários do site OLX usando o scrapy e depois como armazenar em um banco de dados, no caso em questão usamos o [Rethinkdb](http://www.rethinkdb.com/).

### Vamos lá

Agora iremos ver como colocar o nosso projeto Scrapy para rodar em um servidor na nuvem, pois quando você está fazendo um crawler um pouco maior que leva mais tempo para capturar as informações fica inviável deixar ele rodando na sua máquina já que você pode querer desligá-la, reiniciá-la ou pode simplesmente deixar em espera o que iria interromper o processamento.

Existem algumas formas de se colocar um projeto scrapy em um [VPS](https://pt.wikipedia.org/wiki/Servidor_virtual_privado), vou listar algumas:

- Crontab
- Supervisor
- Scrapyd
- Scrapinghub

Por hora eu irei fazer apenas uma pequena apresentação de todas essas opções expandindo apenas a Scrapyd, futuramente irei gravar um vídeo mostrando como utilizar as opções do crontab e supervisor.

#### Crontab

O [crontab](https://pt.wikipedia.org/wiki/Crontab) é um utilitário de sistemas Unix que gerencia comandos que precisam ser executados com alguma periodicidade, assim basta acessar um VPS via ssh, baixar o seu código, instalar as dependências - realizar os passos iniciais presentes nos artigos anteriores - e depois adicionar a tarefa de acordo com o padrão que o crontab aceita (veja o link do [crontab](https://pt.wikipedia.org/wiki/Crontab)).

#### Supervisor

O [Supervisor](http://supervisord.org/) é um sistema desenvolvido em Python que controla a execução de processos. Eu utilizo ele bastante em meus projetos, pois com ele eu tenho como organizar a execução de processos indicando o usuário que irá executar, o diretório de acesso, controle de log e via linha de comando posso iniciar ou terminar o processo de maneira bem simples.

#### Scrapinghub

[Scrapinghub](http://scrapinghub.com/) é a empresa por trás do Scrapy, e essa plataforma dá a possibilidade de você fazer o deploy facilitado de seus crawlers que utilizam o Scrapy, além de visualizar as estatísticas e os dados gerados pelos crawlers.

#### Scrapyd

O [Scrapyd](http://scrapyd.readthedocs.org/en/latest/index.html) é uma aplicação que fornece uma API REST em que você pode fazer upload de seus projetos além de iniciar ou parar a execução de crawlers presentes no seu projeto.

Para utilizar o Scrapyd eu recomendo acessar a sua máquina VPS e em seguida baixar e instalar o Scrapyd.

Considerando que já está no terminal do seu VPS, faça:

Obs1: você pode criar um virtualenv ou se preferir instalar globalmente verifique se está acessando com o usuário **root** ou no grupo **sudo**.
Obs2: linhas com o caractere "$" são comandos executados, linhas sem esse caractere é a saída esperada.

{% highlight sh %}
$ cd /caminho/no/vps/para/o/projeto
$ pip install scrapyd
{% endhighlight %}

Após a instalação do scrapyd, um novo comando estará disponível:

{% highlight sh %}
$ scrapyd
2015-09-07 20:55:03-0400 [-] Log opened.
2015-09-07 20:55:03-0400 [-] twistd 15.2.1 (/usr/bin/python 2.7.6) starting up.
2015-09-07 20:55:03-0400 [-] reactor class: twisted.internet.epollreactor.EPollReactor.
2015-09-07 20:55:03-0400 [-] Site starting on 6800
2015-09-07 20:55:03-0400 [-] Starting factory <twisted.web.server.Site instance at 0x7f883b0adb48>
2015-09-07 20:55:03-0400 [Launcher] Scrapyd 1.0.2 started: max_proc=4, runner='scrapyd.runner'
{% endhighlight %}

Ao rodar este comando você verá que ele irá ativar um servidor web na porta 6800, entretanto você não vai querer rodar o servidor dessa forma, você irá precisar colocar ele em modo daemon para que possa realizar outras atividades e deixá-lo rodando. Como estou acostumado com o supervisor, utilizei ele para monitorar e iniciar o processo do scrapyd - nesse caso ele não vai rodar o crawler em específico, vai rodar o scrapyd e este vai ser responsável pela execução dos crawlers.

Para esse experimento estou utilizando uma máquina com Ubuntu, assim posso instalar o Supervisor dessa forma:

{% highlight sh %}
$ apt-get install supervisor
{% endhighlight %}

Caso utilize outra distribuição Linux procure os pacotes relacionados ao Supervisor ou instale via pip:

http://supervisord.org/installing.html#installing-via-pip

Quando instalado via gerenciador de pacotes da distribuição ele já é executado assim que iniciar a máquina, assim basta criar um arquivo de configuração para o processo relativo ao Scrapyd:

{% highlight sh %}
$ cd /etc/supervisor/conf.d/
$ vi scrapyd.conf
{% endhighlight %}

Em seguida coloque o seguinte conteúdo no arquivo **scrapyd.conf**:

{% highlight sh %}
[program:scrapyd]
command=scrapyd
user=root
autostart=true
{% endhighlight %}

Não é recomendado utilizar o usuário root mas para fins de teste irei indicar este usuário, mas lembre-se de criar um usuário para o scrapyd quando for colocar em produção.

A parte `[program:scrapyd]` indica o nome do programa, vai ser útil na hora de iniciar ou para o processo, o `command=scrapyd` é o comando que irá ser executado, caso esteja utilizando um virtualenv será preciso indicar o caminho do script **scrapyd** relativo ao virtualenv. O `user=root` indica que usuário irá rodar o comando e a opção `autorestart=true` serve para reiniciar o processo sempre que ele "cair", independente do que aconteceu, mais detalhes em:

http://supervisord.org/configuration.html

Agora para ativar o scrapyd iremos executar o comando:

{% highlight sh %}
$ supervisorctl reread
scrapyd: available
$ supervisorctl reload
Restarted supervisord
$ upervisorctl status
scrapyd       RUNNING    pid 1382, uptime 0:00:15
{% endhighlight %}

Agora já podemos acessar a interface web fornecida pelo scrapyd, basta ir no navegador e digitar:

http://&#60;IP-DO-VPS&#62;:6800/

Se tudo deu certo, você verá uma interface extremamente simples, agora saia do VPS e volte a trabalhar localmente.

Acessando a basta do projeto localmente - com o virtualenv ativado caso esteja utilizando, instale:

{% highlight sh %}
$ pip install scrapyd-client
{% endhighlight %}

Com esse pacote iremos ter um facilitador para o deploy do nosso projeto no servidor onde está o scrapyd, pois o scrapyd fornece uma API REST para fazer upload do nosso projeto no formato [EGG](https://wiki.python.org/moin/egg). O scrapyd-client fornece um comando `scrapyd-deploy` que facilita essa geração do egg e em seguida upload para o servidor, assim no arquivo **scrapy.cfg** do seu projeto adicione no final (ou substitua caso já tenha algum valor para a configuração **deploy**):

{% highlight sh %}
[deploy]
url = http://<IP-DO-VPS>:6800/
username = root
password = <senha>
{% endhighlight %}

Em seguida faça o deploy do seu projeto:

{% highlight sh %}
$ scrapyd-deploy -p <nome-do-projeto>
Packing version 1441674561
Deploying to project "<nome-do-projeto>" in http://<IP-DO-VPS>:6800/addversion.json
Server response (200):
{"status": "ok", "project": "<nome-do-projeto>", "version": "1441674561", "spiders": 2, "node_name": "<nome-do-servidor>"}
{% endhighlight %}

Obs: No exemplo da série o nome do projeto é **scrapy_olx**.

Agora você já pode colocar um crawler para rodar, para isso é preciso acessar a API REST do Scrapyd:

{% highlight sh %}
curl http://<IP-DO-VPS>:6800/schedule.json -d project=<nome-do-projeto> -d spider=<nome-do-spider>
{% endhighlight %}

Eu utilizei o [curl](http://curl.haxx.se/), mas você poderia utilizar qualquer ferramenta que possa fazer um GET ou POST dependendo do que deseja fazer, todas as opções da API do Scrapyd, você pode ver em:

http://scrapyd.readthedocs.org/en/latest/api.html

Finalmente podemos ver se o nosso crawler está rodando corretamente acessando a interface web do scrapyd que visualiza os **jobs**:

http://&#60;IP-DO-VPS&#62;:6800/jobs

### Considerações finais

Eu gosto bastante da simplicidade do Scrapyd, entretanto ele não oferece muitas possibilidades para uma melhor visualização dos itens coletados e a interface web se restringe a visualizar, não é possível adicionar spiders e projetos. Além disso, ele deixa "público" o acesso aos jobs e itens - uma forma de burlar isso seria fazendo um proxy com o nginx ou apache e colocando uma autenticação como o [basic http authentication](https://en.wikipedia.org/wiki/Basic_access_authentication).

Esta série acaba por aqui mas em breve irei falar mais sobre esses dados coletados mas o foco não será mais o scrapy, será a análise desses dados.
