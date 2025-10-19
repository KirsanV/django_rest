from rest_framework import viewsets
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Course, Lesson, Subscription
from .serializers import CourseSerializer, LessonSerializer, PaymentSerializer, MessageSerializer
from rest_framework import generics
from users.models import Payment
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from .permissions import IsOwner, IsNotModerator
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .paginators import StandardResultsSetPagination



@extend_schema_view(
    list=extend_schema(
        description='Список курсов',
        responses={200: CourseSerializer(many=True)}
    ),
    create=extend_schema(
        description='Создать курс',
        request=CourseSerializer,
        responses={201: CourseSerializer}
    ),
    update=extend_schema(
        description='Обновить курс',
        responses={200: CourseSerializer}
    ),
    partial_update=extend_schema(
        description='Частичное обновление курса',
        responses={200: CourseSerializer}
    ),
)
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = StandardResultsSetPagination

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

    def perform_update(self, serializer):
        course = serializer.save()
        from .tasks import send_course_update_email
        send_course_update_email.delay(course.id)


@extend_schema_view(
    list=extend_schema(
        description='Список уроков',
        responses={200: LessonSerializer(many=True)}
    ),
    create=extend_schema(
        description='Создать урок',
        request=LessonSerializer,
        responses={201: LessonSerializer}
    ),
)
class LessonListCreate(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Модератор').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


@extend_schema_view(
    retrieve=extend_schema(
        description='Детали урока',
        responses={200: LessonSerializer}
    ),
    update=extend_schema(
        description='Обновить урок',
        request=LessonSerializer,
        responses={200: LessonSerializer}
    ),
    destroy=extend_schema(
        description='Удалить урок',
        responses={204: None}
    ),
)
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


@extend_schema_view(
    list=extend_schema(
        description='Список платежей',
        responses={200: PaymentSerializer(many=True)}
    ),
    retrieve=extend_schema(
        description='Детали платежа',
        responses={200: PaymentSerializer}
    ),
    create=extend_schema(
        description='Создать платеж',
        request=PaymentSerializer,
        responses={201: PaymentSerializer}
    ),
)
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user', 'course', 'lesson', 'payment_method']
    ordering_fields = ['payment_date', 'amount']
    ordering = ['-payment_date']


@extend_schema_view(
    post=extend_schema(
        description='Подписаться/отписаться на курс',
        responses={200: MessageSerializer}
    )
)
class CourseSubscriptionAPIView(APIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course')
        course = get_object_or_404(Course, id=course_id)

        subs_qs = Subscription.objects.filter(user=user, course=course)

        if subs_qs.exists():
            subs_qs.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'подписка добавлена'

        return Response({"message": message})

