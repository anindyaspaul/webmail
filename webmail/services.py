from imbox import Imbox
from django.conf import settings
from webmail.models import EmailMessage
from pprint import pprint
import datetime


class IMAPService():
    def __init__(
        self,
        host=settings.IMAP_HOST,
        username=settings.IMAP_USER,
        password=settings.IMAP_PASSWORD,
        use_ssl=settings.IMAP_USE_SSL
    ):
        self.host = host
        self.username = username
        self.password = password
        self.use_ssl = use_ssl
    
    @property
    def mailbox(self):
        return f'{self.username}@{self.host}'

    def fetch(self, uid_from=1):
        with Imbox(
            self.host,
            username=self.username,
            password=self.password,
            ssl=self.use_ssl,
        ) as imbox:
            imap_messages = imbox.messages(uid__range=f'{uid_from}:*')
            for uid, msg in imap_messages:
                yield uid, msg
