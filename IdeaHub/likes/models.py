from django.db import models
from django.contrib.auth.models import User
from ideas.models import Idea
# Create your models here.

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'idea')  

    def _str_(self):
        return f"{self.user.username} likes {self.idea.title}"