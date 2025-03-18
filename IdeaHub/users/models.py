from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_TYPES = [
        ('idea_owner', 'Idea Owner'),
        ('business', 'Business / Investor')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='idea_owner')
    about = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to="images/avatars/", default="images/avatars/avatar.webp")
    website = models.URLField(blank=True, null=True)
    favorite_ideas = models.ManyToManyField('ideas.Idea', related_name="favorited_by", blank=True)

    def _str_(self) -> str:
        return f"{self.user.username} - {self.get_user_type_display()}"