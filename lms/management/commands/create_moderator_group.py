from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from lms.models import Course, Lesson

class Command(BaseCommand):
    help = 'Создает группу Модераторы и назначает права'

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name='Модератор')
        self.stdout.write(f'Группа {"создана" if created else "уже существует"}: {group.name}')

        content_type_course = ContentType.objects.get_for_model(Course)
        content_type_lesson = ContentType.objects.get_for_model(Lesson)

        permissions_codenames = [
            ('view_course', content_type_course),
            ('change_course', content_type_course),
            ('view_lesson', content_type_lesson),
            ('change_lesson', content_type_lesson),
        ]

        permissions = []
        for codename, c_type in permissions_codenames:
            perm = Permission.objects.get(codename=codename, content_type=c_type)
            permissions.append(perm)

        group.permissions.set(permissions)
        self.stdout.write('Права успешно назначены группе.')