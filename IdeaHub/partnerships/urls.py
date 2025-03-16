from django.urls import path
from . import views

app_name = 'partnerships'

urlpatterns = [
    path('<int:idea_id>/request/', views.request_partnership, name='request'),
    path('<int:partnership_id>/approve/', views.approve_partnership, name='approve'),
]