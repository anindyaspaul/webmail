from django.db import models

# Create your models here.

class EmailMessage(models.Model):
    uid = models.IntegerField()
    msg_id = models.CharField(max_length=255)
    mailbox = models.CharField(max_length=255, null=False)
    sent_on = models.DateTimeField(null=False)
    sent_from = models.JSONField(null=False)
    sent_to = models.JSONField(null=False)
    cc = models.JSONField()
    bcc = models.JSONField()
    subject = models.CharField(max_length=255, null=True)
    body_plain = models.TextField(null=True)
    body_html = models.TextField(null=True)
