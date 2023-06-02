from contracts.models import Contract, Event
from client.models import CustomClient
from core.models import CustomUser
from EpicEvent.permissions import IsManager, ClientPermissions, ContractPermissions, EventPermissions
from contracts.serializer import ContractSerializer, EventSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status

def get_support_related_contracts(user):
    support_contracts = []
    for event in Event.objects.filter(support_contact = user):
        if event.support_contact == user and event.contract:
            support_contracts.append(event.contract.id)
    return Contract.objects.filter(id_in=support_contracts)

class ContractView(viewsets.ModelViewSet):
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, IsManager, ContractPermissions]
    
    def get_queryset(self):
        if self.request.user.usergroup == CustomUser.UserGroupe.SUPPORT:
            return get_support_related_contracts(self.request.user)
        elif self.request.user.usergroup == CustomUser.UserGroupe.SALE:
            return Contract.objects.filter(client_sales_contact=self.request.user)
    
    def create(self, request):
        serializer = ContractSerializer(context={'request': request}, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EventView(ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsManager, EventPermissions]
    
    def get_queryset(self, *args, **kwargs):  
        return Event.objects.filter(contract_id=self.kwargs.get('contract_id'))
    
class EventDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsManager, EventPermissions]
    lookup_field = 'id'
    
    def get_queryset(self, *args, **kwargs):
        if self.request.user.usergroup == CustomUser.UserGroup.SALE:
            return Event.objects.filter(contract_sales_contact=self.request.user)
       
        elif self.request.user.usergroup == CustomUser.UserGroup.SALE:
            return Event.objects.filter(support_contact=self.request.user)

        return Event.objects.filter(event_id=self.kwargs.get('event_id'))