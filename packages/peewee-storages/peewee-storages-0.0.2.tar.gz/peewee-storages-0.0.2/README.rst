.. image:: https://img.shields.io/pypi/v/peewee-storages.svg
    :target: https://pypi.org/project/peewee-storages/
    :alt: PyPI Version


Installation
============
We assume that you already got an `peewee` installed.

Installing with `pip` :

.. code-block:: bash

  pip install peewee-storages

You can try to install from source (maybe there is a bugfix in master that
hasn't been released yet) then the magic incantation you are looking for is:

.. code-block:: bash

  pip install -e 'git+https://github.com/python-folks/peewee-storages.git#egg=peewee-storages'


About
=====
This project provides an FileField and Storages for the `peewee ORM <http://docs.peewee-orm.com/en/latest/>`_  package. 

peewee-storages is a package to provide out of box FielField and some Storages backends 
to provide similar experience as the one when using Django with django-storages

This library is usually compatible with the currently supported versions of
peewee.


Found a Bug? Something Unsupported?
===================================
I suspect that a few of the storage engines in backends/ have been unsupported
for quite a long time. I personally only really need the S3Storage backend but
welcome bug reports (and especially) patches and tests for some of the other
backends.

Issues are tracked via GitHub issues at the `project issue page
<https://github.com/python-folks/peewee-storages/issues>`_.

Documentation
=============
Documentation will be included ASAP.

Contributing
============

#. `Check for open issues
   <https://github.com/python-folks/peewee-storages/issues>`_ at the project
   issue page or open a new issue to start a discussion about a feature or bug.
#. Fork the `peewee-storages repository on GitHub
   <https://github.com/python-folks/peewee-storages>`_ to start making changes.
#. Add a test case to show that the bug is fixed or the feature is implemented
   correctly.
#. Bug me until I can merge your pull request. Also, don't forget to add
   yourself to ``AUTHORS``.