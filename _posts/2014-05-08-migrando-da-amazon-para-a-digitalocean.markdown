---
title: "Migrando da Amazon para a DigitalOcean"
layout: post
permalink: migrando-da-amazon-para-a-digitalocean
author: Gileno Filho
date: 2014-05-08 15:46:00
categories: utils
tags: deploy django
---

Olá pessoal, recentemente migrei alguns sistemas (PyCursos e Pingmind) da [AWS](https://aws.amazon.com/) (Amazon Web Services) para a [DigitalOcean](https://www.digitalocean.com/?refcode=7e3d1a0c801e) e vou falar um pouco sobre essa experiência.


A migração não foi uma decisão fácil, afinal nunca problemas com a AWS - apenas 1 em 2 anos de uso - e a AWS oferece muito mais do que simplesmente uma VPS Linux, ela tem diversos serviços como o [RDS](https://aws.amazon.com/pt/rds/) e o [S3](https://aws.amazon.com/pt/s3/) que tiram a responsabilidade do desenvolvedor de gerenciar alguns recursos e ferramentas. Mas então porque sair da AWS? A primeira coisa é o custo, em muitos casos não irá compensar mas no meu caso passei de uma conta de $ 160 - $ 190 por mês para exatos $ 45 (+ $ 60 por ano do [Vimeo](https://vimeo.com/)), uma economia considerável. Engraçado é que depois que eu mudei para a DigitalOcean o [Linode](https://www.linode.com/) baixa os preços e coloca SSD, se tivesse feito antes é provável que eu voltasse para o Linode (usava ele antes da AWS).


Outro fator é a dependência com a AWS, conversando com um professor da UFPE da área de sistemas distribuídos, ele comentou essa questão da dependência com empresas de Computação na Nuvem. As empresas oferecem diversos serviços extra (considerando que uma VPS é o básico) e quando você precisa mudar sua arquitetura ou trocar de ferramenta você terá muitos problemas, e de fato isto aconteceu comigo. Tive problemas na organização dos arquivos estáticos que antes eram servidos pelo S3 e os vídeos que usavam o [Cloud Front](http://aws.amazon.com/pt/cloudfront/). Felizmente o código está razoavelmente estruturado e genérico - na medida do possível - e para os vídeos que eram o maior problemas migramos para o Vimeo - particularmente uma das melhores coisas que eu já fiz na minha vida.


De modo geral foram esses os argumentos mais fortes que me fizeram fazer essa mgiração, mas houveram outros pequenos detalhes como armazenamento em SSD, API simples e mais direta - existem menos serviços - suporte via e-mail muito bom e uma área para a comunidade com fórum e tutoriais.


No fim, o que eu desejo passar neste post é o seguinte: antes de contratar um provedor de nuvem, análise todos os aspectos técnicos e financeiros dele, por mais que AWS seja muito boa eu me sinto muito mais feliz usando a DigitalOcean pois oferece um ótimo serviço e estou livre para montar minha infra do jeito que eu quiser, e caso eu queira migrar para outro provedor - como o Linode - será muito mais tranquilo. Eu não sou contra ficar preso a alguns tipos de serviços, eu mesmo estou usando o Vimeo e alguns outros serviços como mailchimp, mas são serviços mais gerais, serviços gerenciais e é mais fácil mudar se assim eu desejar.


O próximo passo será organizar minhas instâncias (droplets) na DigitalOcean para fazer auto scale e separar melhor as instâncias que serão responsáveis pelas app's e a instância do banco de dados, já vi alguns tutoriais e será algo divertido e que me trará um aprendizado legal.


Num próximo post eu falo mais detalhes técnicos dessa mudança e explico como está a estrutura de minhas instâncias, de toda forma abaixo segue alguns links interessantes que eu usei, eu já tenho uma experiência legal em montar a infra básica de uma app Django mas é sempre bom ver o que a galera faz por ai, na própria [DigitalOcean](https://www.digitalocean.com/community/) existem muita coisa:

- [http://michal.karzynski.pl/blog/2013/06/09/django-nginx-gunicorn-virtualenv-supervisor/](http://michal.karzynski.pl/blog/2013/06/09/django-nginx-gunicorn-virtualenv-supervisor/)
- [https://www.digitalocean.com/community/articles/how-to-install-and-configure-django-with-postgres-nginx-and-gunicorn](https://www.digitalocean.com/community/articles/how-to-install-and-configure-django-with-postgres-nginx-and-gunicorn)
- [http://pypass.gr/tutorial/django-digitalocean-droplet](http://pypass.gr/tutorial/django-digitalocean-droplet)


*Obs: não estou ganhando nada para falar da DigitalOcean hein :) mas o link acima é com o meu refcode.*
