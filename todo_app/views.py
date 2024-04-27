from django.shortcuts import render, redirect, get_object_or_404
from .models import Task

def index(request):
    # Capture the user's IP address
    ip_address = request.META.get('REMOTE_ADDR')
    tasks = Task.objects.filter(ip_address=ip_address)

    return render(request, 'todo_app/index.html', {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        ip_address = request.META.get('REMOTE_ADDR')
        # Create the task associated with the user's IP address
        Task.objects.create(title=title, description=description, ip_address=ip_address)
    
    return redirect('index')

def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        
        
        if task.ip_address == request.META.get('REMOTE_ADDR'):
            task.title = title
            task.description = description
            task.save()
    
    return redirect('index')

def complete_task(request, task_id):
    task = Task.objects.get(id=task_id)

    if task.ip_address == request.META.get('REMOTE_ADDR'):
        task.completed = True
        task.save()
    
    return redirect('index')

def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    
    if task.ip_address == request.META.get('REMOTE_ADDR'):
        task.delete()
    
    return redirect('index')
