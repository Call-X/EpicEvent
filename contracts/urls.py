from django.urls import path
from contracts.views import ContractView, ContractDetailView, EventView, EventDetailView


create_contract = ContractView.as_view({
     'get': 'list',
     'post': 'create'
 })


urlpatterns = ([
    path('create_contract/', create_contract, name='contract'),
    path('contracts/<int:id>/', ContractDetailView.as_view(), name='detail_contract'),
    path('contract/<int:contract_id>/event/', EventView.as_view()),
    path('contract/<int:contract_id>/event/<int:id>/', EventDetailView.as_view()),
 ])
