from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('professor', 'Professor'),
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student'
    )
    college = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    bio = models.TextField(blank=True)

    def is_professor(self):
        return self.role == 'professor'

    def is_student(self):
        return self.role == 'student'

    def __str__(self):
        return f"{self.username} ({self.role})"