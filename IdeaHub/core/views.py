from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification


def home(request):
    unread_notifications = 0
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(recipient=request.user, is_read=False).count()
    return render(request, 'core/home.html', {'unread_notifications': unread_notifications})

def about(request):  
    return render(request, 'core/about.html')


def contact(request):
    return render(request, 'core/contact.html')


@login_required
def notifications_list(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    
    return render(request, 'core/notifications.html', {'notifications': notifications})


@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    
    return redirect('core:notifications_list')