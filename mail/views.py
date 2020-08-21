from django.shortcuts import render
from django.views import View
from mail.forms import MailForm
from django.core.mail import send_mail
from imbox import Imbox
from django.conf import settings
from datetime import datetime


class HomeView(View):
    template_name = 'inbox.html'
    
    def get(self, request):
        messages = []
        with Imbox(settings.IMAP_HOST,
            username=settings.IMAP_USER,
            password=settings.IMAP_PASSWORD,
            ssl=settings.IMAP_USE_SSL,
        ) as imbox:
            imap_messages = reversed(imbox.messages()[-5:])
            for message_id, message in imap_messages:
                messages.append({
                    'id': int(message_id),
                    'sent_from': message.sent_from[0],
                    'sent_to': message.sent_to,
                    'subject': message.subject,
                    'date': message.date,
                    'body_plain': message.body.get('plain'),
                    'body_html': message.body.get('html', message.body.get('plain')),
                })

        return render(request, self.template_name, { 'messages': messages })



class ComposeView(View):
    template_name = 'compose.html'

    def get(self, request):
        form = MailForm()
        return render(request, self.template_name, { 'form': form })

    def post(self, request):
        form = MailForm(request.POST)
        success = False

        if form.is_valid():
            to = form.cleaned_data.get('to')
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')
            send_mail(subject=subject, message=message, from_email=None, recipient_list=[to])
            success = True

            form = MailForm()

        return render(request, self.template_name, { 'form': form, 'success': success })


class MessageView(View):
    template_name = 'message.html'
    
    def get(self, request):
        message_id = int(request.GET['id'])
        imap_message = None
        with Imbox(settings.IMAP_HOST,
            username=settings.IMAP_USER,
            password=settings.IMAP_PASSWORD,
            ssl=settings.IMAP_USE_SSL,
        ) as imbox:
            imap_message = imbox.messages(uid__range=f'{message_id}:{message_id+1}')[0][1]

        print(imap_message.body.get('html')[0])
        return render(request, self.template_name, { 'message': imap_message.body.get('html')[0]})

