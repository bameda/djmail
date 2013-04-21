.. _settings:

========
Settings
========

Backend
-------

djmail exposes a lot of settings for costumize a great part of default behavior.

**DJMAIL_REAL_BACKEND**

Indicates to djmail which a real email backend use for deliver email messages.

Default: ``django.core.mail.backends.console.EmailBackend``


**DJMAIL_SEND_ASYNC**

Makes a default backend of djmail send emails asyncronouslly (with threads).

Default: False


**DJMAIL_MAX_RETRY_NUMBER**

Set a default maximum retry number for deliver failed messages.

Default: 3


Template Mail
-------------

**DJMAIL_BODY_TEMPLATE_PROTOTYPE**

Prototype for make body template path.

Default: ``email/{name}_body.{ext}``

**DJMAIL_SUBJECT_TEMPLATE_PROTOTYPE**

Prototype for make subject template path.

Default: ``email/{name}_subject.txt``

**DJMAIL_HTML_TEMPLATE_EXTENSION**

Extension used for html rendering

Default: ``html``

**DJMAIL_TXT_TEMPLATE_EXTENSION**

Extension used for text rendering

Default: ``txt``
