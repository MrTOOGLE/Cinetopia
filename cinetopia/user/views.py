from django.shortcuts import render

def auth(request):
    return render(request, 'user/auth.html')
