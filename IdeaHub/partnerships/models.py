from django.db import models
from django.contrib.auth.models import User
from ideas.models import Idea

class Partnership(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='partnerships')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)  # يجب أن يوافق مالك الفكرة على الشراكة
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('idea', 'user')  # كل مستخدم يمكنه طلب الشراكة مرة واحدة فقط لكل فكرة

    def _str_(self):
        return f"{self.user.username} wants to join {self.idea.title}"

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='partnership_notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Notification for {self.recipient.username}"