#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os
import sys

sys.path.append(os.curdir)

from collections import OrderedDict

AUTHOR = u'Gileno Filho'
SITENAME = u'Gileno Filho'
SITEURL = 'http://localhost:8000'

META_DESCRIPTION = '''Website Gileno Filho'''

META_KEYWORDS = [
    'programação', 'python', 'recife', 'desenvolvimento',
    'data science'
]

TIMEZONE = 'America/Recife'
THEME = 'themes/malt'
MALT_BASE_COLOR = 'green'

SITE_LOGO = ''
SITE_LOGO_MOBILE = ''

STATIC_PATHS = ['images', 'extra/CNAME', 'extra/favicon.ico']
EXTRA_PATH_METADATA = {
    'extra/CNAME': {'path': 'CNAME'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
}

WELCOME_TITLE = u'Seja bem vindo ao {}!'.format(SITENAME)
WELCOME_TEXT = u'''
    Programação, Python, Django, Web, Inteligência Artificial, Engenharia de Avaliações, Ensino e Minimalismo. Recife, Brasil
'''
SITE_BACKGROUND_IMAGE = 'images/foto-bairrorecife.jpg'
FOOTER_ABOUT = u'''
    Website e Blog de Gileno Filho, escrevo sobre: Desenvolvimento,
    Python, Django, Ciência de Dados, Engenharia de Avaliações,
    Inteligência Artificial e Design Minimalista.
'''

DEFAULT_LANG = u'pt'

ARTICLE_URL = '{slug}'
ARTICLE_SAVE_AS = '{slug}/index.html'

PAGE_URL = '{slug}'
PAGE_SAVE_AS = '{slug}.html'

CATEGORIES_URL = 'categorias'
CATEGORIES_SAVE_AS = 'categorias/index.html'
CATEGORY_URL = 'categorias/{slug}'
CATEGORY_SAVE_AS = 'categorias/{slug}/index.html'

TAG_URL = 'tags/{slug}'
TAG_SAVE_AS = 'tags/{slug}/index.html'
TAGS_URL = 'tags'
TAGS_SAVE_AS = 'tags/index.html'

AUTHOR_URL = 'autores/{slug}'
AUTHOR_SAVE_AS = 'autores/{slug}/index.html'
AUTHORS_URL = 'autores'
AUTHORS_SAVE_AS = 'autores/index.html'

INDEX_SAVE_AS = "index.html"

PAGINATION_PATTERNS = (
    (1, '{base_name}/', '{base_name}/index.html'),
    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
)

TRANSLATION_FEED_ATOM = None
TRANSLATION_FEED_RSS = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
CATEGORY_FEED_ATOM = None
CATEGORY_FEED_RSS = None

DEFAULT_PAGINATION = 5

PLUGIN_PATHS = []
PLUGINS = []

RESPONSIVE_IMAGES = True
PYGMENTS_STYLE = "perldoc"
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.8,
        'indexes': 0.2,
        'pages': 0.7
    },
    'changefreqs': {
        'articles': 'daily',
        'indexes': 'daily',
        'pages': 'monthly'
    },
}

GITHUB_REPO = "http://github.com/gileno/gileno.github.io"
GITHUB_BRANCH = "pelican"
TWITTER = "@gilenofilho"
OPEN_GRAPH_IMAGE = "images/eu.jpg"

# Navbar Links
NAVBAR_HOME_LINKS = [
    {
        "title": u"Cursos",
        "href": "categorias/cursos/",
    },
    {
        "title": u"Palestas",
        "href": "categorias/palestras/",
    },
    {
        "title": u"Tutoriais",
        "href": "categorias/tutoriais/",
    },
    {
        "title": u"Utils",
        "href": "categorias/utils/",
    },
]

NAVBAR_BLOG_LINKS = NAVBAR_HOME_LINKS + [

]

SOCIAL_LINKS = (
    {
        "href": "https://github.com/gileno",
        "icon": "fa-github",
        "text": "GitHub",
    },
    {
        "href": "https://twitter.com/gilenofilho",
        "icon": "fa-twitter",
        "text": "Twitter",
    },
    {
        "href": "https://www.facebook.com/gilenofilho",
        "icon": "fa-facebook",
        "text": "Facebook",
    },
    {
        "href": "mailto:contato@gilenofilho.com.br",
        "icon": "fa-envelope",
        "text": "E-mail",
    },
)

MEMBROS = OrderedDict((
    (u"Gileno Filho", {
        "email": "contato@gilenofilho.com.br",
        "twitter": "@gilenofilho",
        "github": "gileno"
    }),
))

MALT_HOME = []

from themes.malt.functions import *
