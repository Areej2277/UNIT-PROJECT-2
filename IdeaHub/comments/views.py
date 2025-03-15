from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Comment
from .forms import CommentForm
from ideas.models import Idea

# Create your views here.

@login_required
def add_comment(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.idea = idea
            comment.save()
            return redirect('ideas:list')
    else:
        form = CommentForm()
    return render(request, 'comments/add_comment.html', {'form': form, 'idea': idea})
