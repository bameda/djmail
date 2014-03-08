# -*- coding: utf-8 -*-

from django.core.mail import EmailMessage
from django.core import mail
from django.db import connection
from django.test import TestCase
from django.test.utils import override_settings

from . import models
from . import core
from .template_mail import TemplateMail, MagicMailBuilder


class TestEmailSending(TestCase):
    def setUp(self):
        models.Message.objects.all().delete()

    @override_settings(
        EMAIL_BACKEND="djmail.backends.default.EmailBackend",
        DJMAIL_REAL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_simple_send_email(self):
        email = EmailMessage('Hello', 'Body goes here', 'from@example.com',
                             ['to1@example.com', 'to2@example.com'])

        email.send()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(models.Message.objects.count(), 1)

    @override_settings(
        EMAIL_BACKEND="djmail.backends.async.EmailBackend",
        DJMAIL_REAL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        DJMAIL_SEND_ASYNC=True)
    def test_async_send_email(self):
        email = EmailMessage('Hello', 'Body goes here', 'from@example.com',
                             ['to1@example.com', 'to2@example.com'])
        # If async is activated, send method
        # returns a thread instead of a number of
        # sent messages.
        future = email.send()
        result = future.result()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(models.Message.objects.count(), 1)

    @override_settings(
        EMAIL_BACKEND="djmail.backends.default.EmailBackend",
        DJMAIL_REAL_BACKEND="testing.mocks.BrokenEmailBackend")
    def test_failing_simple_send_email(self):
        email = EmailMessage('Hello', 'Body goes here', 'from@example.com',
                             ['to1@example.com', 'to2@example.com'])

        number_sent_emails = email.send()

        self.assertEqual(number_sent_emails, 0)
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(models.Message.objects.count(), 1)

        mailmodel = models.Message.objects.get()
        self.assertEqual(mailmodel.status, models.STATUS_FAILED)

    @override_settings(
        EMAIL_BACKEND="djmail.backends.async.EmailBackend",
        DJMAIL_REAL_BACKEND="testing.mocks.BrokenEmailBackend")
    def test_failing_async_send_email(self):
        email = EmailMessage('Hello', 'Body goes here', 'from@example.com',
                             ['to1@example.com', 'to2@example.com'])

        f = email.send()
        rs = f.result()

        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(models.Message.objects.count(), 1)

        mailmodel = models.Message.objects.get()
        self.assertEqual(mailmodel.status, models.STATUS_FAILED)

    @override_settings(
        EMAIL_BACKEND="djmail.backends.celery.EmailBackend",
        DJMAIL_REAL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_async_send_email_with_celery(self):
        email = EmailMessage('Hello', 'Body goes here', 'from@example.com',
                             ['to1@example.com', 'to2@example.com'])
        result = email.send()
        result.wait()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(models.Message.objects.count(), 1)

    @override_settings(
        EMAIL_BACKEND="djmail.backends.celery.EmailBackend",
        DJMAIL_REAL_BACKEND="testing.mocks.BrokenEmailBackend")
    def test_failing_async_send_email_with_celery(self):
        email = EmailMessage('Hello', 'Body goes here', 'from@example.com',
                             ['to1@example.com', 'to2@example.com'])
        result = email.send()
        result.wait()

        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(models.Message.objects.count(), 1)

        mailmodel = models.Message.objects.get()
        self.assertEqual(mailmodel.status, models.STATUS_FAILED)

    @override_settings(
        EMAIL_BACKEND="djmail.backends.celery.EmailBackend",
        DJMAIL_REAL_BACKEND="testing.mocks.BrokenEmailBackend")
    def test_failing_retry_send_01(self):
        email = EmailMessage('Hello', 'Body goes here', 'from@example.com',
                             ['to1@example.com', 'to2@example.com'])
        message_model = models.Message.from_email_message(email)
        message_model.status = models.STATUS_FAILED
        message_model.retry_count = 1
        message_model.save()

        core._retry_send_messages()

        message_model_2 = models.Message.objects.get(pk=message_model.pk)
        self.assertEqual(message_model_2.retry_count, 2)

    @override_settings(
        EMAIL_BACKEND="djmail.backends.celery.EmailBackend",
        DJMAIL_REAL_BACKEND="testing.mocks.BrokenEmailBackend",
        DJMAIL_MAX_RETRY_NUMBER=2)
    def test_failing_retry_send_01(self):
        email = EmailMessage('Hello', 'Body goes here', 'from@example.com',
                             ['to1@example.com', 'to2@example.com'])
        message_model = models.Message.from_email_message(email)
        message_model.status = models.STATUS_FAILED
        message_model.retry_count = 3
        message_model.save()

        core._mark_discarted_messages()

        message_model_2 = models.Message.objects.get(pk=message_model.pk)
        self.assertEqual(message_model_2.retry_count, 3)
        self.assertEqual(message_model_2.status, models.STATUS_DISCARTED)


class TestTemplateEmailSending(TestCase):
    def setUp(self):
        models.Message.objects.all().delete()

    @override_settings(
        EMAIL_BACKEND="djmail.backends.default.EmailBackend",
        DJMAIL_REAL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_simple_send_email_1(self):
        class SimpleTemplateMail(TemplateMail):
            name = "test_email1"

        email = SimpleTemplateMail()
        email.send("to@example.com", {"name": "foo"})

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(models.Message.objects.count(), 1)

        m = mail.outbox[0]
        self.assertEqual(m.subject, u'Subject1: foo')
        self.assertEqual(m.alternatives[0][0], u"<b>Mail1: foo</b>\n")

    @override_settings(
        EMAIL_BACKEND="djmail.backends.default.EmailBackend",
        DJMAIL_REAL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_simple_send_email_2(self):
        class SimpleTemplateMail(TemplateMail):
            name = "test_email2"

        email = SimpleTemplateMail()
        email.send("to@example.com", {"name": "foo"})

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(models.Message.objects.count(), 1)

        m = mail.outbox[0]
        self.assertEqual(m.subject, u'Subject2: foo')
        self.assertEqual(m.body, u"body\n")
        self.assertEqual(m.alternatives, [(u'<b>Body</b>\n', 'text/html')])

    @override_settings(
        EMAIL_BACKEND="djmail.backends.default.EmailBackend",
        DJMAIL_REAL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_simple_send_email_with_magic_builder_1(self):
        mails = MagicMailBuilder()

        email = mails.test_email2("to@example.com", {"name": "foo"});
        email.send()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(models.Message.objects.count(), 1)

        self.assertEqual(email.subject, u'Subject2: foo')
        self.assertEqual(email.body, u"body\n")
        self.assertEqual(email.alternatives, [(u'<b>Body</b>\n', 'text/html')])


    @override_settings(
        EMAIL_BACKEND="djmail.backends.default.EmailBackend",
        DJMAIL_REAL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_simple_send_email_with_magic_builder_1_with_low_priority(self):
        mails = MagicMailBuilder()

        email = mails.test_email2("to@example.com", {"name": "foo"}, priority=10);
        email.send()

        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(models.Message.objects.count(), 1)


        m1 = models.Message.objects.get()
        self.assertEqual(m1.status, models.STATUS_PENDING)
        self.assertEqual(m1.priority, 10)

        core._send_pending_messages()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(models.Message.objects.count(), 1)

        m2 = models.Message.objects.get()
        self.assertEqual(m2.status, models.STATUS_SENT)
        self.assertEqual(m2.priority, 10)
