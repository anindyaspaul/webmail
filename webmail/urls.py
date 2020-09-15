from django.urls import path, include
from webmail.views import EmailListView, EmailComposeView, EmailDetailsView, EmailSyncView


urlpatterns = [
    path('', EmailListView.as_view(), name='home'),
    path('compose/', EmailComposeView.as_view(), name='compose'),
    path('details/', EmailDetailsView.as_view(), name='details'),
    path('sync/', EmailSyncView.as_view(), name='sync'),
]
