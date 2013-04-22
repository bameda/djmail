Quickstart
==========

Install
-------

You can download tarball from Pypi_, extract this and install with:

.. _Pypy: http://pypi.python.org/pypi/djmail/


.. code-block:: console

    tar xvf djmail-x.y.tar.gz
    cd djmail
    python setup.py install


Other (recomended) alternative is install with **pip**:

.. code-block:: console

    pip install djmail


Configure
---------

As first step, configure your email backend settings to one of backends
that djmail offers.

djmail works as middleware, so you must configure the true email backend.

Example initial configuration:

.. code-block:: python

    EMAIL_BACKEND="djmail.backends.default.EmailBackend"
    DJMAIL_REAL_BACKEND="django.core.mail.backends.console.EmailBackend"


For usage examples see :ref:`How to use <usage>`
