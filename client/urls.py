from django.urls import path
from client.views import ClientView, ClientDetailView


create_client = ClientView.as_view({
     'get': 'list',
     'post': 'create'
 })

urlpatterns = ([
    path('create_client/', create_client, name='create_client'),
    path('details_client/<int:id>/', ClientDetailView.as_view()),
 ])