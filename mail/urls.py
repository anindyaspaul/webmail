from django.urls import path, include
from conf.views import HomeView


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
