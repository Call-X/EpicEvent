from rest_framework.generics import CreateAPIView
from core.models import CustomUser
from rest_framework.permissions import AllowAny
from core.serializer import UserSerializer

class RegisterView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
