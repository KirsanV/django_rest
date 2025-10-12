from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from lms.models import Course, Lesson

User = get_user_model()

class LessonAPITests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email='user1@example.com', password='pass123')
        self.user2 = User.objects.create_user(email='user2@example.com', password='pass123')
        self.course = Course.objects.create(name='Курс 1', owner=self.user1)
        self.lesson1 = Lesson.objects.create(course=self.course, name='Урок 1', owner=self.user1)
        self.lesson2 = Lesson.objects.create(course=self.course, name='Урок 2', owner=self.user1)
        self.lesson_list_url = reverse('lesson-list')
        self.lesson_detail_url = lambda pk: reverse('lesson-detail', kwargs={'pk': pk})

    def test_list_lessons_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.lesson_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIn('results', response.data)
        self.assertIsInstance(response.data['results'], list)
        self.assertGreaterEqual(len(response.data['results']), 2)

    def test_list_lessons_unauthenticated(self):
        response = self.client.get(self.lesson_list_url)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_create_lesson_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        data = {
            'course': self.course.id,
            'name': 'Новый урок',
            'owner': self.user1.id
        }
        response = self.client.post(self.lesson_list_url, data)
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])
        self.assertTrue(Lesson.objects.filter(name='Новый урок').exists())

    def test_create_lesson_unauthenticated_forbidden(self):
        data = {
            'course': self.course.id,
            'name': 'Новый урок',
            'owner': self.user1.id
        }
        response = self.client.post(self.lesson_list_url, data)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_retrieve_lesson(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.lesson_detail_url(self.lesson1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.lesson1.name)

    def test_update_lesson_owner(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.patch(self.lesson_detail_url(self.lesson1.id), {'name': 'Обновленное имя'})
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_202_ACCEPTED])
        self.lesson1.refresh_from_db()
        self.assertEqual(self.lesson1.name, 'Обновленное имя')

    def test_update_lesson_other_user_forbidden(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.patch(self.lesson_detail_url(self.lesson1.id), {'name': 'Попытка обновления'})
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])

    def test_delete_lesson_owner(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(self.lesson_detail_url(self.lesson1.id))
        self.assertIn(response.status_code, [status.HTTP_204_NO_CONTENT, status.HTTP_200_OK])
        self.assertFalse(Lesson.objects.filter(id=self.lesson1.id).exists())

    def test_delete_lesson_other_user_forbidden(self):
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(self.lesson_detail_url(self.lesson2.id))
        self.assertIn(response.status_code, [status.HTTP_403_FORBIDDEN, status.HTTP_404_NOT_FOUND])