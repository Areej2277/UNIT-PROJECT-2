from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Idea(models.Model):
    CATEGORY_CHOICES = [
        ('tech', 'Technology'),
        ('business', 'Business'),
        ('science', 'Science'),
        ('design', 'Design'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def _str_(self):
        return self.title