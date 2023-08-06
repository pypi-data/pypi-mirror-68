
=============
Frankfurt ORM
=============

.. inclusion-marker-do-not-remove

``Frankfurt`` is an Object-Relational Mapping (ORM) library, built on top of asyncpg. It takes ideas from Django, SQLAlchemy, GiNO, and tortoise-orm.

Source and issue tracker are available at https://gitlab.com/jorgeecardona/frankfurt/issues

Support Python >= 3.7.

Introduction
------------

Frankfurt is an ORM built on top of asyncpg, henceo, it supports only PostgreSQL.

I am taking ideas from Django, SQLAlchemy and tortoise-orm to built this.

Installation
------------

The recommended way to install ``frankfurt`` is via pip

.. code:: bash

    pip install frankfurt

Quickstart
----------

As expected, a model can be defined as follows:

>>> from frankfurt.models import Model
>>> from frankfurt import fields
>>>
>>> class FirstModel(Model):
...    text = fields.CharField(max_length=200)
>>>
>>> m = FirstModel(text='example')
>>> m['text']
'example'
