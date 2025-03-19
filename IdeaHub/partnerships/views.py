from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import PartnershipRequest
from core.models import Notification  
from ideas.models import Idea

# Submit an application to adopt an idea (for companies only)
@login_required
def request_partnership(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)

    if not hasattr(request.user, 'company_profile'):
        messages.error(request, "Only companies can request partnerships.")
        return redirect('ideas:detail', idea_id=idea_id)

    partnership_request, created = PartnershipRequest.objects.get_or_create(
        idea=idea,
        company_owner=request.user,
        idea_owner=idea.user,
        status="Pending"
    )

    if created:
        Notification.objects.create(
            recipient=idea.user,
            message=f"Company {request.user.username} wants to adopt your idea '{idea.title}'."
        )
        messages.success(request, "Partnership request sent successfully!")
    else:
        messages.warning(request, "You have already requested a partnership for this idea.")

    return redirect('ideas:detail', idea_id=idea_id)

# Accept the partnership request
@login_required
def approve_partnership(request, request_id):
    partnership_request = get_object_or_404(PartnershipRequest, id=request_id)

    if partnership_request.idea_owner != request.user:
        messages.error(request, "You are not allowed to approve this request.")
        return redirect('partnerships:received_requests')

    partnership_request.status = "Approved"
    partnership_request.save()

    Notification.objects.create(
        recipient=partnership_request.company_owner,
        message=f"Your partnership request for '{partnership_request.idea.title}' has been approved!"
    )

    messages.success(request, "Partnership request approved successfully!")
    return redirect('partnerships:received_requests')


# Rejection of partnership application
@login_required
def reject_partnership(request, request_id):
    partnership_request = get_object_or_404(PartnershipRequest, id=request_id)

    if partnership_request.idea_owner != request.user:
        messages.error(request, "You are not allowed to reject this request.")
        return redirect('partnerships:received_requests')

    partnership_request.status = "Rejected"
    partnership_request.save()

    Notification.objects.create(
        recipient=partnership_request.company_owner,
        message=f"Your partnership request for '{partnership_request.idea.title}' has been rejected."
    )

    messages.success(request, "Partnership request rejected.")
    return redirect('partnerships:received_requests')


# View incoming requests from idea owners
@login_required
def received_requests(request):
    requests = PartnershipRequest.objects.filter(idea_owner=request.user, status="Pending").order_by("-created_at")

    if not requests.exists():
        messages.info(request, "You have no pending partnership requests.")

    return render(request, "partnerships/received_requests.html", {"requests": requests})


# Display requests sent to business owners
@login_required
def sent_requests(request):
    if not hasattr(request.user, 'company_profile'):
        messages.error(request, "Only companies can access this page.")
        return redirect("home")

    requests = PartnershipRequest.objects.filter(company_owner=request.user).order_by("-created_at")

    if not requests.exists():
        messages.info(request, "You have not sent any partnership requests yet.")

    return render(request, "partnerships/sent_requests.html", {"requests": requests})


# View notifications
@login_required
def notifications_list(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by("-created_at")

    if not notifications.exists():
        messages.info(request, "No new notifications.")

    return render(request, 'core/notifications.html', {"notifications": notifications})

@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    return redirect('core:notifications_list')