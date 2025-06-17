from django.shortcuts import render, redirect
from django.contrib.auth import logout

def account(request):
    return render(request, 'user/account.html')

def user_logout(request):
    logout(request)
    return redirect('homepage')
