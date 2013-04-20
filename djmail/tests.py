# -*- coding: utf-8 -*-

from django.core.mail import EmailMessage
from django.core import mail
from django.db import connection
from django.test import TestCase
from django.test.utils import override_settings

from . import models
from . import core


class TestEmailSending(TestCase):
    def setUp(self):
        models.Message.objects.all().delete()

    @override_settings(EMAIL_BACKEND="djmail.backends.default.EmailBackend",
                       DJMAIL_REAL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
                       DJMAIL_SEND_ASYNC=False)
    def test_simple_send_email(self):
        email = EmailMessage('Hello', 'Body goes here', 'from@example.com',
                             ['to1@example.com', 'to2@example.com'])

        email.send()
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(models.Message.objects.count(), 1)


    @override_settings(EMAIL_BACKEND="djmail.backends.default.EmailBackend",
                       DJMAIL_REAL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
                       DJMAIL_SEND_ASYNC=True)
    def test_async_send_email(self):
        email = EmailMessage('Hello', 'Body goes here', 'from@example.com',
                             ['to1@example.com', 'to2@example.com'])
        # If async is activated, send method
        # returns a thread instead of a number of
        # sent messages.
        thread = email.send()
        thread.join()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(models.Message.objects.count(), 1)

    @override_settings(EMAIL_BACKEND="djmail.backends.default.EmailBackend",
                       DJMAIL_REAL_BACKEND="testing.mocks.BrokenEmailBackend",
                       DJMAIL_SEND_ASYNC=False)
    def test_failing_simple_send_email(self):
        email = EmailMessage('Hello', 'Body goes here', 'from@example.com',
                             ['to1@example.com', 'to2@example.com'])

        number_sent_emails = email.send()

        self.assertEqual(number_sent_emails, 0)
        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(models.Message.objects.count(), 1)

        mailmodel = models.Message.objects.get()
        self.assertEqual(mailmodel.status, models.STATUS_FAILED)

    @override_settings(EMAIL_BACKEND="djmail.backends.default.EmailBackend",
                       DJMAIL_REAL_BACKEND="testing.mocks.BrokenEmailBackend",
                       DJMAIL_SEND_ASYNC=True)
    def test_failing_async_send_email(self):
        email = EmailMessage('Hello', 'Body goes here', 'from@example.com',
                             ['to1@example.com', 'to2@example.com'])

        thread = email.send()
        thread.join()

        self.assertEqual(len(mail.outbox), 0)
        self.assertEqual(models.Message.objects.count(), 1)

        mailmodel = models.Message.objects.get()
        self.assertEqual(mailmodel.status, models.STATUS_FAILED)

    @override_settings(EMAIL_BACKEND="djmail.backends.celery.EmailBackend",
                       DJMAIL_REAL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_async_send_email_with_celery(self):
        email = EmailMessage('Hello', 'Body goes here', 'from@example.com',
                             ['to1@example.com', 'to2@example.com'])
        result = email.send()
        result.wait()

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(models.Message.objects.count(), 1)


    @override_settings(EMAIL_BACKEND="djmail.backends.celery.EmailBackend",
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

    @override_settings(EMAIL_BACKEND="djmail.backends.celery.EmailBackend",
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

    @override_settings(EMAIL_BACKEND="djmail.backends.celery.EmailBackend",
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
