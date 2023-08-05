.. This file is a part of the AnyBlok / Delivery project
..
..    Copyright (C) 2018 Franck Bret <franckbret@gmail.com>
..    Copyright (C) 2018 Jean-Sebastien SUZANNE <jssuzanne@anybox.fr>
..    Copyright (C) 2019 Jean-Sebastien SUZANNE <js.suzanne@gmail.com>
..
.. This Source Code Form is subject to the terms of the Mozilla Public License,
.. v. 2.0. If a copy of the MPL was not distributed with this file,You can
.. obtain one at http://mozilla.org/MPL/2.0/.

Anyblok Delivery
================

.. image:: https://img.shields.io/pypi/pyversions/anyblok_delivery.svg?longCache=True
    :alt: Python versions

.. image:: https://travis-ci.org/AnyBlok/AnyBlok-Delivery.svg?branch=master
    :target: https://travis-ci.org/AnyBlok/AnyBlok-Delivery
    :alt: Build status

.. image:: https://coveralls.io/repos/github/AnyBlok/AnyBlok-Delivery/badge.svg?branch=master
    :target: https://coveralls.io/github/AnyBlok/AnyBlok-Delivery?branch=master
    :alt: Coverage status

.. image:: https://img.shields.io/pypi/v/anyblok_delivery.svg
   :target: https://pypi.python.org/pypi/anyblok_delivery/
   :alt: Version status

.. image:: https://readthedocs.org/projects/anyblok-delivery/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://doc.anyblok-delivery.anyblok.org/?badge=latest

Delivery management



Features
--------

* TODO

Package dependencies
--------------------

* anyblok_mixins
* anyblok_postgres
* anyblok_attachment
* anyblok_address

Bloks
-----

+------------------------+----------------------+------------------------------------------------------------------+
| Blok                   | Dependancies         | Description                                                      |
+========================+======================+==================================================================+
| **delivery**           | * **attachment**     | Main blok to define what a delivery, an account, a delivery type |
|                        | * **address**        |                                                                  |
|                        | * **anyblok-mixins** |                                                                  |
+------------------------+----------------------+------------------------------------------------------------------+
| **delivery_colissimo** | **delivery**         | Add delivery type: Colissimo                                     |
+------------------------+----------------------+------------------------------------------------------------------+

Author
------

Franck Bret
~~~~~~~~~~~

* franckbret@gmail.com
* https://github.com/franckbret

Contributors
------------

Jean-Sébastien Suzanne
~~~~~~~~~~~~~~~~~~~~~~

* js.suzanne@gmail.com
* https://github.com/jssuzanne
* https://github.com/AnyBlok

Credits
-------

.. _`Anyblok`: https://github.com/AnyBlok/AnyBlok

This `Anyblok`_ package was created with `audreyr/cookiecutter`_ and the `AnyBlok/cookiecutter-anyblok-project`_ project template.

.. _`AnyBlok/cookiecutter-anyblok-project`: https://github.com/Anyblok/cookiecutter-anyblok-project
.. _`audreyr/cookiecutter`: https://github.com/audreyr/cookiecutter
