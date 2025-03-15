from django.db import models
from django.contrib.auth.models import User
from ideas.models import Idea

# Create your models here.

class Comment(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f'Comment by {self.user.username} on {self.idea.title}'