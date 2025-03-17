from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Partnership, Notification
from ideas.models import Idea

@login_required
def request_partnership(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)

    # التحقق إذا كان المستخدم قد طلب الشراكة من قبل
    partnership, created = Partnership.objects.get_or_create(user=request.user, idea=idea)

    if created:
        # إرسال إشعار إلى مالك الفكرة
        Notification.objects.create(
            recipient=idea.user,
            message=f"{request.user.username} has requested to partner with your idea '{idea.title}'."
        )
    else:
        partnership.delete()  # حذف الطلب إذا كان قد تم إرساله مسبقًا

    return redirect('ideas:list')

@login_required
def approve_partnership(request, partnership_id):
    partnership = get_object_or_404(Partnership, id=partnership_id)

    # التأكد من أن المستخدم هو صاحب الفكرة
    if partnership.idea.user == request.user:
        partnership.is_approved = True
        partnership.save()

        # إرسال إشعار إلى المستخدم الذي طلب الشراكة
        Notification.objects.create(
            recipient=partnership.user,
            message=f"Your partnership request for '{partnership.idea.title}' has been approved!"
        )

    return redirect('ideas:list')

@login_required
def notifications_list(request):
    notifications = request.user.notifications.all().order_by('-created_at')
    return render(request, 'notifications/list.html', {'notifications': notifications})

@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications:list')