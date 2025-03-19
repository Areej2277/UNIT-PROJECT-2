from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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

    def __str__(self) -> str:
        return f"{self.user.username} - {self.get_user_type_display()}"
    
    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_profile(sender, instance, **kwargs):
        instance.profile.save()
    
