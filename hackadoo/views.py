from django.shortcuts import render


def home(request):
    user = request.user

    return render(request, 'index.html', context={'user': user})
