# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['uuid', 'from_email', 'to_email', 'status', 'priority', 'created_at', 'sent_at', 'retry_count']
    list_filter = ['status', 'priority', 'created_at', 'sent_at', 'retry_count']
    search_fields = ['from_email', 'to_email', 'subject', 'uuid']
    date_hierarchy = 'created_at'
