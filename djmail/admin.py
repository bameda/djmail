# -*- encoding: utf-8 -*-

from django.contrib import admin
from . import models


class MessageAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'status', 'priority', 'created_at', 'sent_at', 'retry_count')
    list_display_links = list_display

    list_filter = ('status', 'priority', 'created_at', 'sent_at', 'retry_count')

admin.site.register(models.Message, MessageAdmin)
