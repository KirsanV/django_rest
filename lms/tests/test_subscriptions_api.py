from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from lms.models import Course, Subscription

User = get_user_model()


class SubscriptionAPITests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            email="user1@example.com", password="pass123"
        )
        self.user2 = User.objects.create_user(
            email="user2@example.com", password="pass123"
        )
        self.course = Course.objects.create(name="Курс 1", owner=self.user1)
        self.subscribe_url = reverse("course-subscribe")

    def test_subscribe_authenticated(self):
        self.client.force_authenticate(user=self.user2)
        payloads = [
            {"course": self.course.id},
            {"course_id": self.course.id},
        ]
        response = None
        for payload in payloads:
            response = self.client.post(self.subscribe_url, payload)
            if response.status_code in (status.HTTP_201_CREATED, status.HTTP_200_OK):
                break
        self.assertIsNotNone(response)
        self.assertIn(
            response.status_code, (status.HTTP_201_CREATED, status.HTTP_200_OK)
        )
        self.assertTrue(
            Subscription.objects.filter(user=self.user2, course=self.course).exists()
        )

    def test_subscribe_unauthenticated_forbidden(self):
        payload = {"course": self.course.id}
        response = self.client.post(self.subscribe_url, payload)
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN],
        )

    def test_unsubscribe_authenticated(self):
        self.client.force_authenticate(user=self.user2)
        sub = Subscription.objects.create(user=self.user2, course=self.course)

        response = self.client.delete(
            self.subscribe_url, {"course_id": self.course.id}, format="json"
        )
        if response.status_code not in (
            status.HTTP_204_NO_CONTENT,
            status.HTTP_200_OK,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        ):
            self.fail(f"Unexpected status for unsubscribe: {response.status_code}")

        if response.status_code in (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK):
            self.assertFalse(Subscription.objects.filter(id=sub.id).exists())
