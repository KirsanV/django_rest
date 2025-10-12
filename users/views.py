from rest_framework import generics, viewsets, permissions
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer, UserSerializer
from .permissions import IsOwner

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return UserSerializer
        return UserRegistrationSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.IsAdminUser()]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsOwner()]
        else:
            return [permissions.IsAuthenticated()]
