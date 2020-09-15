from django import forms


class EmailComposeForm(forms.Form):
    to = forms.EmailField(required=True, label="To")
    subject = forms.CharField(required=True, label="Subject", max_length=255)
    message = forms.CharField(required=True, label="Message", widget=forms.Textarea)
