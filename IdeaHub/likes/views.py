from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Like
from ideas.models import Idea

# Create your views here.

@login_required #اذا المستخدم مو مسجل بيتوجهه الى صفحة التسجيل
def like_idea(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)
    like, created = Like.objects.get_or_create(user=request.user, idea=idea)

    if not created:  # إذا كان المستخدم قد ضغط إعجاب من قبل يتم إزالته
        like.delete()

    return redirect('ideas:list')