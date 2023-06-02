from django.urls import path
from contracts.views import ContractView, EventView, EventDetailView


create_contract = ContractView.as_view({
     'get': 'list',
     'post': 'create'
 })

detail_contract = ContractView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
 })

urlpatterns = ([
    path('create_contract/', create_contract, name='contract'),
    path('contracts/<int:pk>/', detail_contract, name='detail_contract'),
    path('contract/<int:contract_id>/event/', EventView.as_view()),
    path('contract/<int:contract_id>/event/<int:id>/', EventDetailView.as_view()),
 ])
