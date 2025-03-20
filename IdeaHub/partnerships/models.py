from django.db import models
from django.contrib.auth.models import User
from ideas.models import Idea

# Corporate profile
class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="company_profile")
    company_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def _str_(self):
        return self.company_name

# Partnership application form
class PartnershipRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name="partnership_requests")
    company_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="partnership_requests")
    idea_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_partnership_requests")
    percentage_share = models.PositiveIntegerField(default=10)
    company_location = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('idea', 'company_owner')  # # It is not possible to submit more than one application for each idea from the same company.

    def __str__(self):
        return f"{self.company_owner.username} requested partnership on {self.idea.title}"