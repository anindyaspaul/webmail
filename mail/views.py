from django.shortcuts import render
from django.views import View
from mail.forms import MailForm
from django.core.mail import send_mail


class HomeView(View):
    template_name = 'base.html'
    
    def get(self, request):
        return render(request, self.template_name)


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
