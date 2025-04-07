from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from ideas.models import Idea
from .models import Notification, ContactMessage
from django.contrib import messages

# Homepage view
def home(request):
    unread_notifications = 0
    user_type = None
    top_liked_ideas = Idea.objects.order_by('-likes')[:6]  # Get top 6 most liked ideas

    # If user is logged in, get their unread notifications and type
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(recipient=request.user, is_read=False).count()
        if hasattr(request.user, 'profile'):
            user_type = request.user.profile.user_type

    return render(request, 'core/home.html', {
        'unread_notifications': unread_notifications,
        'user_type': user_type,
        'top_liked_ideas': top_liked_ideas,
    })

# About page
def about(request):
    return render(request, 'core/about.html')

# Contact form handling
def contact(request):
    if request.method == 'POST':
        # Get form fields from request
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save the contact message in the database
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        # Display success message and redirect to contact page
        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact')

    return render(request, 'core/contact.html')

# List of notifications for the logged-in user
@login_required
def notifications_list(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    return render(request, 'core/notifications.html', {'notifications': notifications})

# Mark a specific notification as read
@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    return redirect('core:notifications_list')

# Admin-only view to see all contact messages
@staff_member_required
def contact_messages_list(request):
    messages_list = ContactMessage.objects.order_by('-sent_at')
    return render(request, 'core/contact_messages.html', {'messages': messages_list})