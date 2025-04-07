from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Comment
from ideas.models import Idea

# Add a comment on an idea
@login_required
def add_comment(request, idea_id):
    idea = get_object_or_404(Idea, id=idea_id)

    if request.method == 'POST':
        content = request.POST.get("content", "").strip()

        if content:
            comment = Comment.objects.create(
                user=request.user,
                idea=idea,
                content=content
            )
            messages.success(request, "Comment added successfully!", "alert-success")
        else:
            messages.error(request, "Comment cannot be empty!", "alert-danger")

        return redirect('ideas:detail', idea_id=idea.id)

    return render(request, 'comments/add_comment.html', {'idea': idea})


# Delete comment
@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Make sure the user is the commenter
    if request.user != comment.user:
        messages.error(request, "You are not authorized to delete this comment.", "alert-danger")
        return redirect('ideas:detail', idea_id=comment.idea.id)

    if request.method == "POST":
        comment.delete()
        messages.success(request, "Comment deleted successfully!", "alert-warning")
        return redirect('ideas:detail', idea_id=comment.idea.id)

    return render(request, 'comments/delete_comment.html', {'comment': comment})