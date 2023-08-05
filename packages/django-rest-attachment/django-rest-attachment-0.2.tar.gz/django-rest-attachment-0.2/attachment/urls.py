from django.urls import path
from .views import download

app_name = 'attachment'

urlpatterns = [
    path('download/<int:pk>/', download, name='download')
]
