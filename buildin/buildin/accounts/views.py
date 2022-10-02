from django.shortcuts import render

def user_login(request):
    return render (request, 'accounts/login.html')

def user_register(request):
    return render (request, 'accounts/register.html')

def profile_details(request, pk):
    return render (request, 'accounts/profile-details.html')

def profile_edit(request, pk):
    return render (request, 'accounts/profile-edit.html')
