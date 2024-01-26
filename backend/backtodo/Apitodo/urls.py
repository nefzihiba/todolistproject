from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.manageTasks, name='task-list-create'),
    path('tasks/<int:pk>/update/', views.manageTask, name='task-update'),
    path('tasks/<int:pk>/delete/', views.manageTask, name='task-delete'),
]
