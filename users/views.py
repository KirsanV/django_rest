from rest_framework import generics, viewsets, permissions
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer, UserSerializer, PaymentCreateSerializer, StripePaymentSerializer
from .permissions import IsOwner
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view
from .stripe_service import prepare_payment_for_stripe
from rest_framework.views import APIView

User = get_user_model()


@extend_schema(
    request=UserRegistrationSerializer,
    responses={201: UserSerializer}
)
class UserRegistrationView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=201)


@extend_schema_view(
    list=extend_schema(
        description='Список пользователей (админ)',
        responses={200: UserSerializer(many=True)}
    ),
    retrieve=extend_schema(
        description='Детали пользователя',
        responses={200: UserSerializer}
    ),
)
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


class StripePaymentCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PaymentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment = serializer.save(user=request.user)

        domain = request.get_host()
        scheme = 'https' if request.is_secure() else 'http'

        try:
            payment = prepare_payment_for_stripe(payment, domain=domain, scheme=scheme)
        except Exception as e:
            return Response({'detail': str(e)}, status=400)

        return Response({
            'payment': StripePaymentSerializer(payment).data,
            'checkout_url': payment.stripe_payment_url
        }, status=201)
