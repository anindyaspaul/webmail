from django.urls import path, include
from mail.views import HomeView, ComposeView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('compose/', ComposeView.as_view(), name='compose'),
]
