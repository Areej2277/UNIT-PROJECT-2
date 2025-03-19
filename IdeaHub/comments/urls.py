from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('<int:idea_id>/add/', views.add_comment, name='add'),
    path('<int:comment_id>/delete/', views.delete_comment, name='delete'),

]