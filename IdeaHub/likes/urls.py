from django.urls import path
from . import views

app_name = 'likes'

urlpatterns = [
    path('<int:idea_id>/like/', views.like_idea, name='like'),
]