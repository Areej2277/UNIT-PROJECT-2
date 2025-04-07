from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Idea
from .forms import IdeaForm
from likes.models import Like

# Create your views here.


def idea_list(request):
    category = request.GET.get('category', None)

    if category:
        ideas = Idea.objects.filter(category=category).order_by('-created_at')
    else:
        ideas = Idea.objects.all().order_by('-created_at')
    liked_ideas = {idea.id: idea.likes.filter(user=request.user).exists() for idea in ideas} if request.user.is_authenticated else {}
    return render(request, 'ideas/idea_list.html', {'ideas': ideas, 'liked_ideas': liked_ideas})



@login_required
def idea_create(request):
    if request.method == 'POST':
        form = IdeaForm(request.POST)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.user = request.user  
            idea.save()
            messages.success(request, "Your idea has been submitted successfully!")
            return redirect('ideas:list')
    else:
        form = IdeaForm()
    return render(request, 'ideas/idea_create.html', {'form': form})



@login_required
def idea_edit(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id, user=request.user)
    if request.method == 'POST':
        form = IdeaForm(request.POST, instance=idea)
        if form.is_valid():
            form.save()
            return redirect('ideas:list')
    else:
        form = IdeaForm(instance=idea)
    return render(request, 'ideas/idea_edit.html', {'form': form, 'idea': idea})


@login_required
def idea_delete(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id, user=request.user)
    if request.method == 'POST':
        idea.delete()
        return redirect('ideas:list')
    return render(request, 'ideas/idea_delete.html', {'idea': idea})

def idea_detail(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)
    return render(request, 'ideas/detail.html', {'idea': idea})