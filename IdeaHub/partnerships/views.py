from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Partnership
from ideas.models import Idea

# Create your views here.

@login_required
def request_partnership(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)
    
    # Check if the user has requested a partnership before
    partnership, created = Partnership.objects.get_or_create(user=request.user, idea=idea)

    if not created:
        partnership.delete()
    
    return redirect('ideas:list')

@login_required
def approve_partnership(request, partnership_id):
    partnership = get_object_or_404(Partnership, id=partnership_id)

    # Check if the user is the owner of the idea
    if partnership.idea.user == request.user:
        partnership.is_approved = True
        partnership.save()

    return redirect('ideas:list')