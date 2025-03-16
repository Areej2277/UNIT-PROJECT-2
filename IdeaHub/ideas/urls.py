from django.urls import path
from . import views

app_name = 'ideas'  

urlpatterns = [
    path('', views.idea_list, name='list'),
    path('create/', views.idea_create, name='create'), 
    path('<int:idea_id>/edit/', views.idea_edit, name='edit'),
    path('<int:idea_id>/delete/', views.idea_delete, name='delete'),
     path('<int:idea_id>/detail/', views.idea_detail, name='detail'),
]