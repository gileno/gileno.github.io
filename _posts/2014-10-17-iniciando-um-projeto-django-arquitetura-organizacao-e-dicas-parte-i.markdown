---
title: "Iniciando um projeto Django (Arquitetura, Organização e Dicas) - Parte I"
layout: post
permalink: iniciando-um-projeto-django-arquitetura-organizacao-e-dicas-parte-i
date: 2014-10-17 11:29
author: Gileno Filho
categories: tutoriais
tags: python django
---

Olá pessoal, quando eu comecei a trabalhar com Django uma das minha maiores dúvidas era em relação a arquitetura de um projeto, organização dos arquivos, diretórios e coisas do tipo. O comando **django-admin.py startproject** só criava 4 arquivos e eu ficava com dúvida em como seria a arquitetura de um grande projeto. Eu estava acostumado com a burocracia de Java e C#, eram muitas classes abstratas e interfaces, acredito que hoje isso tenha melhorado mas na minha época era muita complexidade, tanto que eu usava template de projeto que não conseguia entender boa parte do código e isso era algo que me fazia infeliz nessas linguagens, mas isso fica para outro artigo.

Felizmente eu comecei a trabalhar no [Atepassar](https://pt-br.facebook.com/AtePassar), esse projeto foi fechado por problemas internos mas isso é outra história. Lá eu vi que a simplicidade com que eu usava Django não era porque eu estava começando, para meu espanto Django era simples mesmo, assim como Python. Entretanto tinham alguns detalhes na organização do projeto que na época não eram muito claros para mim. Havia liberdade mas como eu era iniciante eu queria alguma indicação de como organizar meu projeto.

Hoje se você procurar por "[django template project](http://lmgtfy.com/?q=django+template+project)" no google, vai ver diversos exemplos de projetos e a partir da versão 1.4 foi disponibilizada uma forma de no [startproject](https://docs.djangoproject.com/en/dev/ref/django-admin/#django-admin-startproject) indicar a estrutura inicial do projeto, que já foi um grande avanço na organização do projeto.

Primeiramente eu irei mostrar o template de projeto que eu utilizo: https://github.com/gileno/django-template-project. A versão desse post vai até o commit: https://github.com/gileno/django-template-project/tree/ad4c0978a09cd8aa510e1555f06baf53a5ee9faa, como estou sempre atualizando o master já não está tão simples.

Para usá-lo, rode o **startproject** da seguinte forma:

<pre>django-admin startproject --template=https://github.com/gileno/django-template-project/archive/master.zip --extension=conf --name=Makefile --name=local_settings.py.example project_name</pre>


Substitua o *project_name* pelo nome do seu projeto. Esse meu template tem uma base de um outro criado pelo [Allisson](https://twitter.com/allisson):

https://github.com/allisson/django-project-template

Eu adaptei para algumas necessidades minhas e adicionei algumas funções, templatetag's e uma app base, **core**. Nessa primeira parte eu vou apresentar apenas a estrutura base do projeto e a app **core**.

A estrutura base não tem uma pasta para para os templates pois eu uso a pasta **templates** dentro da app **core** a mesma coisa eu faço para os arquivos estáticos, usando a pasta **static**, isso evita criar uma pasta templates e uma static fora das apps, além de evitar alterar duas settings: *TEMPLATES_DIRS* e *STATIC_DIRS*.

Eu também adiciono um Makefile para algumas tarefas, normalmente têm mais opções mas esse do template é uma versão simplificada. Além disso, vão alguns arquivos de configuração que serão utilizados no servidor, como o **nginx.conf** e o **supervisor.conf**, por fim adiciono um gunicorn_start que é um shell script que será utilizado para levantar o processo do gunicorn.

Enfim, nesta primeira parte eu mostrei apenas a base do template de projeto que eu utilizo, ainda faltam alguns utilitários, como: funções, templatetag's, models...

Parte II - http://gilenofilho.com.br/iniciando-um-projeto-django-arquitetura-organizacao-e-dicas-parte-ii/

Atualizado: Ao postar esse artigo no PUG-PE o [João](http://www.dirtycoder.net) me indicou o [cookiecutter](https://github.com/audreyr/cookiecutter) e mencionou que existe um para o django [cookiecutter-django](https://github.com/pydanny/cookiecutter-django). Por hora o sistema atual do django é suficiente para mim e eu costumo ser preguiçoso, isto é, procuro o mais simples e direto possível, mas no final da série é provável que faça uma versão final usando o cookiecutter.

### Curso de Django
No dia 11 de novembro irá iniciar uma nova turma do meu curso de Django pelo PyCursos. Iremos utilizar Python 3 e a versão mais atual do Django 1.6 e 1.7. Mais detalhes em:

http://pycursos.com/django/
