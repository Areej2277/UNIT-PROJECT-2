from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('<int:idea_id>/add/', views.add_comment, name='add'),
]