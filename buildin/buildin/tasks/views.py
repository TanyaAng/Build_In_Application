from django.shortcuts import render


def task_create(request):
    return render(request, 'tasks/task-create.html')


def task_edit(request, pk):
    return render (request, 'tasks/task-edit.html')


def task_delete(request, pk):
    return render (request, 'tasks/task-delete.html')
