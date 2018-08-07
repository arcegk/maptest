from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('add-address', views.AddressAditionView.as_view(), name='add_address')
]
