from rest_framework import viewsets
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from rest_framework import generics
from users.models import Payment
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from .permissions import IsOwner, IsNotModerator
from rest_framework.permissions import IsAuthenticated


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.IsAdminUser]
        elif self.action == 'retrieve':
            return [permissions.IsAuthenticated(), IsOwner()]
        elif self.action == 'create':
            return [permissions.IsAuthenticated(), IsNotModerator()]
        elif self.action in ['update', 'partial_update']:
            return [permissions.IsAuthenticated(), IsOwner()]
        elif self.action == 'destroy':
            return [permissions.IsAuthenticated(), IsOwner()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Модератор').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListCreate(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Модератор').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class LessonRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Модератор').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user', 'course', 'lesson', 'payment_method']
    ordering_fields = ['payment_date', 'amount']
    ordering = ['-payment_date']


