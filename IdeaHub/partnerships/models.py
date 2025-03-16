from django.db import models
from django.contrib.auth.models import User
from ideas.models import Idea

# Create your models here.

class Partnership(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='partnerships')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)  # The idea owner must agree to the partnership.
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('idea', 'user')  #Each user can only request a partnership once.

    def _str_(self):
        return f"{self.user.username} wants to join {self.idea.title}"