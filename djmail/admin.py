from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['subject', 'from_email', 'to_email', 'status', 'created_at', 'sent_at']
    list_filter = ['status', 'created_at', 'sent_at']
    search_fields = ['subject', 'from_email', 'to_email']
    date_hierarchy = 'created_at'
    readonly_fields = ['uuid', 'subject', 'status', 'from_email', 'to_email', 'body_text', 'body_html', 'body_html_show', 'priority', 'retry_count', 'created_at', 'sent_at', 'exception']
    
    fields = ['subject', 'status', 'from_email', 'to_email', 'body_text', 'body_html_show', 'created_at', 'sent_at']
    
    @mark_safe
    def body_html_show(self, instance):
        return instance.body_html
    body_html_show.short_description = "Body html"
