from django.db import models
from django.conf import settings
from django.utils import timezone


class Event(models.Model):
    CATEGORY_CHOICES = (
        ('technical', 'Technical'),
        ('cultural', 'Cultural'),
        ('sports', 'Sports'),
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
        ('hackathon', 'Hackathon'),
        ('other', 'Other'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    college = models.CharField(max_length=200)
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='other'
    )
    date = models.DateTimeField()
    venue = models.CharField(max_length=300, blank=True)
    max_participants = models.PositiveIntegerField(default=100)
    image = models.ImageField(
        upload_to='event_images/',
        blank=True,
        null=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='events'
    )
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title

    def is_upcoming(self):
        return self.date > timezone.now()

    def registered_count(self):
        return self.registrations.count()

    def is_full(self):
        return self.registered_count() >= self.max_participants

    def get_category_color(self):
        colors = {
            'technical': '#6C63FF',
            'cultural': '#FF6584',
            'sports': '#43E97B',
            'workshop': '#F7971E',
            'seminar': '#4FACFE',
            'hackathon': '#FA709A',
            'other': '#A8EDEA',
        }
        return colors.get(self.category, '#6C63FF')


class Registration(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='registrations'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='registrations'
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevent duplicate registration
        unique_together = ('event', 'user')
        ordering = ['-registered_at']

    def __str__(self):
        return f"{self.name} → {self.event.title}"