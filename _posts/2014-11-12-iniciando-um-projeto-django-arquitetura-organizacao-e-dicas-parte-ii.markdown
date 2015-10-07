---
title: "Iniciando um projeto Django (Arquitetura, Organização e Dicas) - Parte II"
layout: post
permalink: iniciando-um-projeto-django-arquitetura-organizacao-e-dicas-parte-ii
date: 2014-11-12 19:37:00
author: Gileno Filho
categories: tutoriais
tags: python django
---

Parte I - http://gilenofilho.com.br/iniciando-um-projeto-django-arquitetura-organizacao-e-dicas-parte-i/

Olá pessoal, na primeira parte desta série eu mostrei a motivação desta série e como usar um template de projeto django para iniciar seu projeto com uma estrutura inicial melhor do que a básica fornecida pelo django.

Nesta segunda parte eu atualizei o repositório do projeto adicionando uma view básica na app **core** e adicionei uma templatetag de paginação bem simples que eu uso em alguns projetos. Existem algumas apps para paginação mas por simplicidade eu utilizo essa templatetag.

Repositório: https://github.com/gileno/django-template-project

A templatetag de paginação é de fácil uso e funciona com a generic view: [ListView](https://docs.djangoproject.com/en/1.7/ref/class-based-views/generic-display/#listview). Ela precisa que esteja no contexto do template as variáveis **paginator** e **page_obj** que é o padrão da [ListView](https://docs.djangoproject.com/en/1.7/ref/class-based-views/generic-display/#listview).

Também adicionei a app [Model Mommy](https://model-mommy.readthedocs.org/en/latest/) que é simplesmente fantástica para teste, é aquela típica app que você se pergunta porque não criou antes.

No models.py da app **core** adicionei um model base que tem dois campos, uma para armazenar a data de criação e outro para a data de modificação, normalmente todos os models herdam dele.

Na próxima parte eu irei adicionar uma app de usuários usando o sistema de compatibilidade de django. Eu não gosto de usar a padrão do django por causa da não obrigatoriedade do campo e-mail no User e pela necessidade de criar um outro model sempre que precisar armazenar mais informações do usuário, como foto, cpf ...
