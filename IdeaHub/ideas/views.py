from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Idea
from .forms import IdeaForm

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Idea
from .forms import IdeaForm


def idea_list(request):
    ideas = Idea.objects.all().order_by('-created_at')  
    return render(request, 'ideas/idea_list.html', {'ideas': ideas})


@login_required
def idea_create(request):
    if request.method == 'POST':
        form = IdeaForm(request.POST)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.user = request.user  
            idea.save()
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