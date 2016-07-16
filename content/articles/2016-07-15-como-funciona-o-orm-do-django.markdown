---
layout: post
title: Como funciona o ORM do Django
slug: como-funciona-o-orm-do-django
date: 2016-07-18 09:00:00
author: Gileno Filho
category: tutoriais
tags: django,database
---

Uma das coisas mais interessantes do framework [Django](https://djangoproject.com/) é sem dúvidas o seu [ORM](https://pt.wikipedia.org/wiki/Mapeamento_objeto-relacional). E o que o torna interessante é a sua simplicidade e objetividade quando se utiliza os [Lookups](https://docs.djangoproject.com/en/1.9/ref/models/lookups/) para realizar consultas simples e até as complexas que envolvem join's.

Neste artigo irei explorar algumas coisas básicas para quem está iniciando mas também irei mostrar casos de uso mais avançados como uso de funções próprias do banco de dados. Para demonstrar as consultas irei utilizar uma modelagem simples para uma aplicação de atividades realizadas, os modelos estão abaixo:


```
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.IntegerField()
    class Meta:
        db_table = 'users'
    def __str__(self):
        return self.name

class Activity(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    special = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    class Meta:
        db_table = 'activities'
    def __str__(self):
        return '[{}] {}'.format(self.user, self.title)
```

Dados de teste:

<table class="table">
    <thead>
        <th>id</th>
        <th>name</th>
        <th>email</th>
        <th>age</th>
    </thead>
    <tbody>
    <tr><td>1</td><td>Gileno Filho</td><td>contato@gilenofilho.com.br</td><td>28</td></tr>
    <tr><td>2</td><td>Admin</td><td>admin@admin.com</td><td>30</td></tr>
    <tr><td>3</td><td>Fulano</td><td>fulano@gilenofilho.com.br</td><td>18</td></tr>
    </tbody>
</table>

<table class="table">
    <thead>
        <th>id</th>
        <th>user</th>
        <th>title</th>
        <th>date</th>
        <th>start_time</th>
        <th>end_time</th>
        <th>special</th>
        <th>score</th>
    </thead>
    <tbody>
    <tr>
        <td>1</td><td>Gileno Filho</td><td>escrever</td>
        <td>10/07/2016</td><td>10:00</td><td>13:00</td>
        <td>True</td><td>4</td>
    </tr>
    <tr>
        <td>2</td><td>Gileno Filho</td><td>gravar</td>
        <td>11/07/2016</td><td>12:00</td><td>17:00</td>
        <td>True</td><td>3</td>
    </tr>
    <tr>
        <td>3</td><td>Admin</td><td>gerenciar</td>
        <td>12/07/2016</td><td>10:00</td><td>12:00</td>
        <td>False</td><td>2</td>
    </tr>
    <tr>
        <td>4</td><td>Fulano</td><td>nadar</td>
        <td>12/07/2016</td><td>15:00</td><td>17:00</td>
        <td>False</td><td>1</td>
    </tr>
    <tr>
        <td>5</td><td>Fulano</td><td>passear</td>
        <td>15/07/2016</td><td>10:00</td><td>11:00</td>
        <td>True</td><td>5</td>
    </tr>
    </tbody>
</table>

Para acessar qualquer objeto salvo no banco de dados é preciso acessar primeiro o `Manager` do `Model`, isto é, o atributo `objects` presente em todo `Model`. Esse `Manager` tem diversos métodos que no final de contas vão chamar um objeto do tipo `QuerySet`, este é que fica responsável pelas consultas de fato. Eu vou separar a explicação das consultas por partes:

- [Consultas Simples](#simples)
- [Consultas Relacionamento](#relacionamento)
- [Aggregate e Annotate](#aggregation)
- [Consultas Manuais](#manuais)
- [Funções do Banco de Dados](#funcoes)

<a id="simples"></a>
### Consultas Simples

O principal método da `QuerySet` é o `filter`, o `Manager` tem um atalho para ele com o mesmo nome. Com esse método você irá realizar as consultas passando as condições da seguinte forma:

```
>>> User.objects.filter(NOMEDOCAMPO__LOOKUP)
```

Os dois underlines/underscores servem para indicar ao Django qual o nome do campo e qual o lookup será utilizado, pois o django vai receber esse parâmetro de forma dinâmica, também conhecido como parâmetros `**kwargs` de uma função. Abaixo seguem alguns exemplos de uso com os modelos definidos anteriormente:

Com o lookup `icontains` eu posso filtrar campos de texto procurando por parte da palavra, no caso qualquer usuário que tenha a palavra `gileno` no nome.

```
>>> User.objects.filter(name__icontains='gileno')
[<User: Gileno Filho>]
```

O `icontains` é apenas um dos lookups disponíveis, para ver todos os lookups possívels acesse: [https://docs.djangoproject.com/en/1.9/ref/models/querysets/#field-lookups](https://docs.djangoproject.com/en/1.9/ref/models/querysets/#field-lookups)

No entanto é comum realizar consultas que verificam mais de um campo, para condições do tipo ***AND*** é possível utilizar o `filter` normalmente apenas indicando separando as condições com vírgula, isto é, passando vários parâmetros de uma vez ou realizar a consulta encadeada:

```
>>> import datetime as dt
>>> start_time = dt.time(10)
>>> Activity.objects.filter(start_time=start_time, title='gerenciar')
[<Activity: [Admin] gerenciar>]
>>> Activity.objects.filter(start_time=start_time).filter(title='gerenciar')
[<Activity: [Admin] gerenciar>]
```

Para consultas do tipo ***OR*** é necessário chamar o objeto `Q`, ele é o responsável por transcrever a consulta que será realizada. Quando utilizamos o `filter` ele é chamado de forma implicíta, para utilizar de forma explicíta basta passá-lo como parâmetro posicional no `filter`:

```
>>> from django.db.models import Q
>>> User.objects.filter(Q(email__icontains='@gilenofilho.com.br'))
[<User: Gileno Filho>, <User: Fulano>]
>>> Activity.objects.filter(Q(title='nadar') | Q(title='gerenciar'))
[<Activity: [Admin] gerenciar>, <Activity: [Fulano] nadar>]
```

A barra vertical entre as duas chamadas de `Q` serve para criar o ***OR*** entre as condições, isto funciona porque o objeto `Q` implementa o método mágico `__or__`. Essa é a grande sacada das melhores libs e frameworks Python, utilizar-se dos métodos mágicos para sobreescrever operadores e açucares sintáticos previstos na definição de Python. É possível combinar ***OR*** e ***AND*** até que a consulta deseja seja gerada, para usar o ***AND*** basta utilizar o `&` ao invés da barra vertical.

```
>>> from django.db.models import Q
>>> user_fulano = User.objects.get(pk=3)
>>> Activity.objects.filter(Q(user=user_fulano) & (Q(special=True) | Q(title='nadar')))
[<Activity: [Fulano] nadar>, <Activity: [Fulano] passear>]
```

Alguns lookups são específicos para determinados tipos de dados, como o `range` que verificar se uma determinada data está entre 2 datas especificadas:

```
>>> import datetime as dt
>>> start_date = dt.date(2016, 7, 10)
>>> end_date = dt.date(2016, 7, 11)
>>> Activity.objects.filter(date__range=(start_date, end_date))
[<Activity: [Gileno Filho] escrever>, <Activity: [Gileno Filho] gravar>]
```

<a id="relacionamento"></a>
### Consultas Relacionamento

O objeto `Q` além de entender diversos lookups, ele também entende quando o atributo a ser utilizado na condição é uma ***ForeignKey*** e deseja-se aplicar a condição sobre um valor presente no objeto relacionado. Para isto utiliza-se novamente o dois underlines/underscores, assim ele irá realizar o join necessário para a consulta encadeada:

```
>>> Activity.objects.filter(user__email='admin@admin.com')
[<Activity: [Admin] gerenciar>]
>>> Activity.objects.filter(user__email__icontains='@gilenofilho.com.br')
[<Activity: [Gileno Filho] escrever>, <Activity: [Gileno Filho] gravar>, <Activity: [Fulano] nadar>, <Activity: [Fulano] passear>]
```

Em todo relacionamento o Django cria o acesso inverso, isto é, se o model `Activity` tem um atributo chamado `user` que faz o relacionamento com a classe `User`, o `User` terá um atributo criado automaticamente com o padrão:

```
nome_da_classe_set
```

Assim é possível acessar os objetos da classe `Activity` através de uma instância de `User`:

```
>>> gileno = User.objects.get(pk=1)
>>> gileno.activity_set.all()
[<Activity: [Gileno Filho] escrever>, <Activity: [Gileno Filho] gravar>]
```

Esse atributo é uma `QuerySet` previamente filtrada e que pode ser aplicado outras condições como qualquer `QuerySet`.

As consultas que envolvem relacionamentos também permitem realizar o fluxo inverso, isto é, filtrar a classe *filha* para depois consultar a classe *mãe*. Isto é bastante útil quando você deseja obter objetos que tem algum tipo de pré-requisito relacionado aos seus *filhos*:

```
>>> activities = Activity.objects.filter(special=True).values_list('user')
>>> activities
[(1,), (1,), (3,)]
>>> User.objects.filter(pk__in=activities)
[<User: Gileno Filho>, <User: Fulano>]
```

O objeto `activities` é um tipo especial de `QuerySet` que armazena apenas o valor dos campos indicados na chamada do `values_list`.

<a id="aggregation"></a>
### Aggregate e Annotate

Como o nome já diz, o ***Aggregate*** irá agregar o resultado de uma consulta em apenas uma linha, normalmente apenas um valor. Na prática se utiliza quando deseja-se somar, verificar o máximo e mínimo, contar e outras operações semelhantes:

```
>>> from django.db.models import Max, Min, Sum
>>> Activity.objects.aggregate(Max('date'), Min('date'))
{'date__max': datetime.date(2016, 7, 15), 'date__min': datetime.date(2016, 7, 10)}
>>> User.objects.aggregate(total_age=Sum('age'))
{'total_age': 76}
```

O retorno do `aggregate` é um dicionário, e caso a chamada for com parâmetros não nomeados ele gera a chave para cada valor de acordo com o nome do atributo e o tipo do *Aggregate*.

Já o ***Annotate*** serve para adicionar informações no objeto que está sendo consultado, como no exemplo abaixo:

```
>>> from django.db.models import Count
>>> users = User.objects.annotate(Count('activity'))
>>> for u in users:
>>>     print(u.activity__count)
>>>
2
1
2
```

Isso funciona porque o model `User` sabe que tem um relacionamento com o model `Activity`, você consegue ver isso de forma dinâmica acessando a meta informação sobre a classe:

```
>>> User._meta.get_fields()
(<ManyToOneRel: core.activity>,
 <django.db.models.fields.AutoField: id>,
 <django.db.models.fields.CharField: name>,
 <django.db.models.fields.EmailField: email>,
 <django.db.models.fields.IntegerField: age>)
```

O ***annotate*** é bastante poderoso, por exemplo se eu quisesse as últimas atividades cadastradas do usuário, isto é, as atividades com maior ID para cada usuario. Primeiro eu precisaria fazer um select das atividades agrupadas por usuário para em seguida pegar o ID máximo. Com ***annotate*** eu posso fazer assim:

```
>>> from django.db.models import Max
>>> pks = Activity.objects.values('user').annotate(max_pk=Max('pk'))
>>> pks
[{'user': 1, 'max_pk': 2}, {'user': 2, 'max_pk': 3}, {'user': 3, 'max_pk': 5}]
>>> Activity.objects.filter(pk__in=pks.values('max_pk'))
[<Activity: [Gileno Filho] gravar>, <Activity: [Admin] gerenciar>, <Activity: [Fulano] passear>]
```

Com o aggregate e annotate eu também posso fazer o ***group by*** em Django:

```
>>> from django.db.models import Avg, Sum
>>> users = Activity.objects.values('user__name')
>>> users.annotate(total_score=Sum('score'), avg_score=Avg('score'))
[{'total_score': 2, 'user__name': 'Admin', 'avg_score': 2.0}, {'total_score': 6, 'user__name': 'Fulano', 'avg_score': 3.0}, {'total_score': 7, 'user__name': 'Gileno Filho', 'avg_score': 3.5}]
```

<a id="manuais"></a>
### Consultas Manuais

Mesmo com tantas possibilidades que o ORM do Django nos fornece, algumas vezes precisamos fazer uma consulta mais "manual". Podemos realizar consultas utilizando o método `extra` da seguinda forma:

```
>>> sql = "users.id in (select activities.user_id from activities where activities.special=%s)"
>>> User.objects.extra(where=[sql], params=[True])
[<User: Gileno Filho>, <User: Fulano>]
```

No caso acima não era realmente necessário escrever o SQL da clásula *where* manualmente, mas eu o fiz para demonstrar que se não for possível realizar alguma consulta com os métodos descritos anteriormente, você pode utilizar o método `extra` e escrever a consulta de forma manual. Lembrando que no caso é preciso saber o nome da tabela e se houver parâmetros devem ser passados como no exemplo para que o Django faça o *escape* para evitar [SQL Injection](https://pt.wikipedia.org/wiki/Inje%C3%A7%C3%A3o_de_SQL).

O Django também permite se realizar uma consulta *raw*, isto é, você faz toda a consulta SQL e só vai indicar o modelo que irá representar o resultado dessa consulta, isso é possível utilizando o método `raw`.

```
>>> users = User.objects.raw('select name, email, age from users')
>>> for user in users:
        print(user)

Gileno Filho
Admin
Fulano
```

O uso do `raw` é interessante quando existe alguma consulta mais complexa em que os valores do campos virão de outras tabelas ou de algum cálculo de alguma função no banco de dados, assim basta que o resultado da consulta tenha os campos que o model tenha.

<a id="funcoes"></a>
### Funções do Banco de Dados

Em geral, os bancos de dados relacionais, têm uma série de funções que auxiliam a criação de scripts SQL. Se você deseja utilizar essas funções para fazer cálculos diretamente no seu [SGBD](https://pt.wikipedia.org/wiki/Sistema_de_gerenciamento_de_banco_de_dados), o Django permite da seguinte forma:

```
from django.db import models

class TimeDiff(models.Func):

    function = 'timediff'
    output_field = models.TimeField()
```

O parâmetro `function` é o nome da função no banco de dados, nesse exemplo esto considerando um banco de dados MySQL onde existe essa função. O parâmetro `output_field` indica que tipo de `Field` será retornado.

```
>>> activities = Activity.objects.annotate(duration=TimeDiff('end_time', 'start_time'))
>>> for activity in activities:
        print(activity.duration)
03:00:00
05:00:00
02:00:00
02:00:00
01:00:00
```

Ainda existe mais coisas a se explorar no ORM do Django mas eu vou parar por aqui, espero que esse artigo lhe ajude a compreender mais as opções que o ORM do Django disponibiliza. Se tiver outras dicas ou críticas comenta ai :)

---

<div class="thumbnail">
    <a href="https://www.udemy.com/construa-um-e-commerce-com-python-3-e-django/?couponCode=websitegilenofilho">
        <img src="/images/django-udemy-large.jpg" alt="Construa um E-Commerce com Python e Django" class="img-responsive" />
    </a>
    <div class="caption">
        <h3><a href="https://www.udemy.com/construa-um-e-commerce-com-python-3-e-django/?couponCode=websitegilenofilho">Quer aprender Django desenvolvendo um projeto real desde a concepção até o deploy seguindo as melhores práticas do mercado?</a></h3>
        <p>Com o conhecimento adquirido neste curso será possível tirar seus projetos do papel, criando incríveis aplicações web com Python/Django além de utilizar as melhores práticas do mercado, pois iremos desenvolver uma aplicação real chamada Django E-Commerce - uma plataforma de comércio eletrônico. Vamos passar por diversos problemas encontrados no desenvolvimento web, desde a concepção do projeto ao deploy num servidor real.</p>
    </div>
</div>
