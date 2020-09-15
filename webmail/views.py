from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, resolve_url
from django.views import View
from markdown import markdown

from webmail.forms import EmailComposeForm
from webmail.models import EmailMessage
from webmail.services import IMAPService


class EmailListView(View):
    template_name = 'email_list.html'
    
    def get(self, request):
        imap_service = IMAPService()
        email_messages = EmailMessage.objects.filter(mailbox=imap_service.mailbox).order_by('-sent_on')
        paginator = Paginator(email_messages, 25)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        return render(request, self.template_name, { 'page': page, 'last_page_number': paginator.num_pages })


class EmailDetailsView(View):
    template_name = 'email_details.html'
    
    def get(self, request):
        email_id = int(request.GET['id'])
        email = EmailMessage.objects.get(id=email_id)
        return render(request, self.template_name, { 
            'sent_froms': email.sent_from,
            'sent_tos': email.sent_to,
            'date': email.sent_on,
            'subject': email.subject,
            'body': email.body_html or email.body_plain
        })


class EmailComposeView(View):
    template_name = 'email_compose.html'

    def get(self, request):
        form = EmailComposeForm()
        return render(request, self.template_name, { 'form': form })

    def post(self, request):
        form = EmailComposeForm(request.POST)
        success = False

        if form.is_valid():
            to = form.cleaned_data.get('to')
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')
            message_html = markdown(message, extensions=['nl2br'])
            send_mail(subject=subject, message=message, html_message=message_html, from_email=None, recipient_list=[to])
            success = True

            form = EmailComposeForm()

        return render(request, self.template_name, { 'form': form, 'success': success })


class EmailSyncView(View):
    def get(self, request):
        email_messages = []
        imap_service = IMAPService()
        latest_email = EmailMessage.objects.filter(mailbox=imap_service.mailbox).order_by('-uid').first()
        imap_messages = imap_service.fetch(uid_from=getattr(latest_email, 'uid', 0)+1)
        for uid, msg in imap_messages:
            email_msg = EmailMessage(
                uid=int(uid),
                msg_id=msg.message_id,
                mailbox=imap_service.mailbox,
                sent_on=msg.parsed_date,
                sent_from=msg.sent_from,
                sent_to=msg.sent_to,
                cc=msg.cc,
                bcc=msg.bcc,
                subject=getattr(msg, 'subject', None),
                body_plain=next(iter(msg.body.get('plain')), None),
                body_html=next(iter(msg.body.get('html')), None),
            )
            email_messages.append(email_msg)
        EmailMessage.objects.bulk_create(email_messages)
        return redirect(to=resolve_url('home'))
