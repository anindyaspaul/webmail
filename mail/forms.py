from django import forms


class MailForm(forms.Form):
    to = forms.EmailField(required=True, label="To")
    subject = forms.CharField(required=True, label="Subject", max_length=128)
    message = forms.CharField(required=True, label="Message", widget=forms.Textarea)
