from django.db import models
from django.contrib.auth.models import User
from ideas.models import Idea

# User classification (idea owner - company)
class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="company_profile")
    company_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def _str_(self):
        return self.company_name

#Subscription request form
class PartnershipRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name="partnership_requests")
    company_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="partnership_requests")
    idea_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_partnership_requests")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('idea', 'company_owner')  # Each company can submit one application per idea.
    def _str_(self):
        return f"{self.company_owner.username} requested partnership on {self.idea.title}"
