from django.db import models


class EmailRecord(models.Model):

    username = models.CharField(max_length=16)
    mail_message = models.TextField()
    ip = models.GenericIPAddressField()
    mail_state = models.CharField(max_length=16)
    reason = models.TextField(blank=True)
    created_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "email_records"
        verbose_name = "email_record"
        verbose_name_plural = "email_records"
        ordering = ("username", "created_time", )
