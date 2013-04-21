.. _usage:

==========
How to use
==========

djmail works as middleware, and basic usage of this not requires any modification of your
code. Also, it provides some usefull features as:

* render and send emails with templates (with i18n)
* assign priority.

.. note::

   Email objects with low priority are not sended inmediatelly, instead,
   are delayed until the next scheduled shipment (with cron or celery)


Email delivery backends
-----------------------

djmail provides basically two backends: **default** and **celery**.

The default backend works in two modes: standard and async. On stantard mode, the email is sended
inmediatelly in the same thread (in blocking mode) and if its failed, it automatically stored
on a database with **failed state**.

On async mode, djmail creates a separate thread and send a email on it with same behavior with
failing messages.

The celery backend uses celery tasks to send emails and its always send asyncronous. Obviously, with
same behavior as default backend with failing email messages.

.. note::

    All sended email objects are stored on a database with corresponding state, retry count,
    priority, etc...


Email retry methods
-------------------

djmail exposes two methods for delivery failed messages: cron and celery periodic tasks. Each email
is going to try to deliver as maximum number of retries. For set custom retry number or other settings,
see :ref:`Settings section <settings>`.

If you choice is cron, you need execute this management command every N min/sec:

.. code-block:: console

    python manage.py djmail_retry_send_messages


But if you choice is celery periodic tasks, you need put a new entry on `CELERYBEAT_SCHEDULE`:

.. code-block:: python

    from datetime import timedelta

    CELERYBEAT_SCHEDULE = {
        'djmail-retry-120-seconds': {
            'task': 'tasks.retry_send_messages',
            'schedule': timedelta(seconds=120),
        },
    }


Render emails with templates
----------------------------

djmail exposes two clases for build email objects with templates:

* djmail.template_mail.TemplateMail
* djmail.template_mail.MagicMailBuilder


TemplateMail
^^^^^^^^^^^^

The ``TemplateMail`` is a low level implementation, you can define your own TemplateMail subclases.

Example:

.. code-block:: python

    class SomeTemplateEmail(template_mail.TemplateMail):
        name = "some_email"

    # Usage
    email = SomeTemplateEmail()
    email.send("to@example.com", {"template": "context"})

    # Or obtain a native django email object
    email = SomeTemplateEmail().make_email_object("to@example.com",
                                                  {"template": "context"})
    email.send()

As this example, ``TemplateMail`` by default search these templates:

* **emails/some_email_body.html**
* **emails/some_email_body.txt**
* **emails/some_email_subject.txt**

Text version of email body is omited if template does not exists.

See the :ref:`Settings section <settings>` for costumize this behavior.


MagicMailBuilder
^^^^^^^^^^^^^^^^

This is a more powerfull usage of this feature. **MagicMailBuilder** delegate a email
object construction to a **TemplateMail** and exposes more dynamic api.

This example represents the same behavior as previos example:

.. code-block:: python

    mails = template_mail.MagicMailBuilder()

    email = mails.some_email("to@example.com", {"template": "context"})
    email.send()

MagicMailBuilder instance build dynamicaly a method, whose name represents
a name of email. Calling this method, returns a native django email instance.

But it has one feature that TemplateMail does not have, on **to** parameter you
can pass a model instance that represents a User. This model must have email field.

.. code-block:: python

    class MyUser(models.Model):
        email = models.CharField(max_length=200)
        lang = models.CharField(max_length=200, default="es")
        # [...]

    user = MyUser.objects.get(pk=1)
    email = mails.some_email(user, {"template": "context"})


If you user class has email/lang field with other names, you can customize it
with some parameters to a constructor of MagicMailBuilder:

.. code-block:: python

    class MyUser(models.Model):
        personal_email = models.CharField(max_length=200)
        language = models.CharField(max_length=200, default="es")
        # [...]

    user = MyUser.objects.get(pk=1)

    mails = template_mail.MagicMailBuilder(email_attr="personal_email"
                                           lang_attr="language")
    email = mails.some_email(user, {"template": "context"})


I18n
^^^^

Both api's implements i18n for rendering email body and subject. For activate a
specific languate you need pass ``lang`` attribute on a context parameter.

Example:

.. code-block:: python

    email = mails.some_email("to@example.com",
                             {"template": "context", "lang": "es"})

Also, if you use a User model instead of email address on a **to** field, if these
user model contains a **lang** field, djmail use it automatically.


Priority
^^^^^^^^

The dinamic methods generated by **MagicMailBuilder**, accept **priority** as optional
keyworkd argument (by default the priorty is 50) with which can specify the priority.

Priority lower than 20, not sended inmediatelly.

.. code-block:: python

    email = mails.some_email("to@example.com", {"template": "context"},
                             priority=100)
