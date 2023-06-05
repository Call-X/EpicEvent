from client.models import CustomClient
from core.models import CustomUser
from client.serializer import CustomClientSerializer
from contracts.models import Contract
from EpicEvent.permissions import ClientPermissions, IsManager
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from contracts.views import get_support_related_contracts
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, status

# Return clients linked to events we are responsible for
def get_support_related_clients(user):
    clients = []
    for contract in get_support_related_contracts(user):
        if contract.client:
            clients.append(contract.client.id)
    return CustomClient.objects.filter(id_in=clients)

class ClientView(viewsets.ModelViewSet):
    serializer_class = CustomClientSerializer
    queryset = Contract.objects.all()
    permission_classes = [IsAuthenticated, IsManager, ClientPermissions]
    
    def create(self, request):
        serializer = CustomClientSerializer(context={'request': request}, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ClientListView(ListCreateAPIView):
    serializer_class = CustomClientSerializer
    permission_classes = [IsAuthenticated, IsManager, ClientPermissions]

    def get_queryset(self, *args, **kwargs):  
        return CustomClient.objects.filter(client_id=self.kwargs.get('client_id'))


class ClientDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = CustomClientSerializer
    permission_classes = [IsAuthenticated, IsManager, ClientPermissions]
    lookup_field = 'id'
    
    def get_queryset(self):

        """
        SALE Users can access their own clients, and all prospects
        """
        if self.request.user.usergroup == CustomUser.UserGroupe.SALE:
            clients = CustomClient.objects.filter(sales_contact=self.request.user)
            prospects = CustomClient.objects.filter(is_prospect=True)
            return prospects | clients
        if self.request.user.usergroup == CustomUser.UserGroupe.SUPPORT:
            return get_support_related_clients(self.request.user)
            # The following is for Managers to still Access All clients, permissions will prevent access to
            # Unauthorized Usergroups
        return CustomClient.objects.filter(client_id=self.kwargs.get('client_id'))

    
    