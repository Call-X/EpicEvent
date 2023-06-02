from django.urls import path
from core.views import RegisterView
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView


urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("login/refresh/", TokenRefreshView.as_view(), name='token_refresh'),
]