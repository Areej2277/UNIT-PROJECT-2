from django.urls import path
from . import views

app_name = 'partnerships'

urlpatterns = [
    path('<int:idea_id>/request/', views.request_partnership, name='request'),
    path('<int:request_id>/approve/', views.approve_partnership, name='approve'),
    path('<int:request_id>/reject/', views.reject_partnership, name='reject'),
    path('received/', views.received_requests, name='received_requests'),
    path('sent/', views.sent_requests, name='sent_requests'),
]