from django.contrib import admin
from django.template.defaultfilters import truncatechars_html

from .models import EmailRecord


class EmailRecordAdmin(admin.ModelAdmin):
    """Manage mail message in the admin site
    """
    list_display = ('username', 'mail_message_preview', 'ip', 'mail_state', 'created_time')
    readonly_fields = ('username', 'ip', 'mail_message',)
    list_filter = ('username',)
    list_per_page = 20

    def mail_message_preview(self, obj):
        return truncatechars_html(obj.mail_message, '64')


admin.site.register(EmailRecord, EmailRecordAdmin)
