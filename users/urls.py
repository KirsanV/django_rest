from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserRegistrationView, StripePaymentCreateView

router = DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="user-register"),
    path(
        "payments/stripe/create/",
        StripePaymentCreateView.as_view(),
        name="stripe-payment-create",
    ),
    path("", include(router.urls)),
]
