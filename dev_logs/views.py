from django import http
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Project, Entry
from .forms import ProjectForm, EntryForm

# Create your views here.
def index(request):
    """The hompage for Dev Logs"""
    return render(request, 'dev_logs/index.html')

@login_required
def projects(request):
    """Show all of the projects"""
    projects = Project.objects.filter(owner=request.user).order_by('date_added')
    context = {'projects' : projects}
    return render(request, 'dev_logs/projects.html', context)

@login_required
def project(request, project_id):
    """Show a single project and all it's entries"""
    project = Project.objects.get(id=project_id)
    # Make sure the project belongs to the logged in user
    if project.owner != request.user:
        raise Http404
    entries = project.entry_set.order_by('-date_added')
    context = {'project' : project, 'entries' : entries}
    return render(request, 'dev_logs/project.html', context)

@login_required
def new_project(request):
    """Add a new project."""
    if request.method != 'POST':
        # No data, create blank form
        form = ProjectForm()
    else:
        # POST sumbmited data; process data
        form = ProjectForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('dev_logs:projects')
    
    # Display a blank form
    context = {'form' : form}
    return render(request, 'dev_logs/new_project.html', context)

@login_required
def new_entry(request, project_id):
    """Add a new entry to a project"""
    project = Project.objects.get(id=project_id)

    if request.method != 'POST':
        # No data, create blank form
        form = EntryForm()
    else:
        # POST submited data; process data
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            # new_entry.project = project
            new_entry.owner = request.user
            new_entry.save()
            return redirect('dev_logs:project', project_id=project_id)
    
    # Display a blank form
    context = {'project' : project, 'form' : form}
    return render(request, 'dev_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry"""
    entry = Entry.objects.get(id=entry_id)
    project = entry.project
    if project.owner != request.user:
        raise Http404

    if request != 'POST':
        # Initial request; pre-fill form with the current entry
        form = EntryForm(instance=entry)
    else:
        # POST data submited; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('dev_logs:project', project_id=project.id)

    context = {'entry' : entry, 'project' : project, 'form' : form}
    return render(request, 'dev_logs/edit_entry.html', context)