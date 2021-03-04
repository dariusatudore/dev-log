"""Defined URL patterns for learning_logs."""
from django.urls import path

from . import views

app_name = 'dev_logs'
urlpatterns = [
    # Home Page
    path('', views.index, name='index'),
    # Page that shows all projects
    path('projects/', views.projects, name='projects'),
    # Entries page for each project
    path('projects/<int:project_id>/', views.project, name='project'),
    # Page for adding a new porject
    path('new_project/', views.new_project, name='new_project'),
    # Page for adding a new entry
    path('new_entry/<int:project_id>', views.new_entry, name='new_entry'),
    # Page for editing an entry
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
]