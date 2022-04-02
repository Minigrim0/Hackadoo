from django.shortcuts import render
from users.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from users.forms import UserLoginForm


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(email=form.cleaned_data['email'].lower())
            if user.count() == 0:
                messages.add_message(
                    request, messages.ERROR,
                    "The email address or the password is incorrect"
                )
            else:
                user = user.first()
                authuser = authenticate(username=user.username, password=form.cleaned_data['password'])
                if authuser:
                    login(request, authuser)
                    next = request.GET.get("next", reverse('home'))
                    return HttpResponseRedirect(next)
                else:
                    messages.add_message(
                        request, messages.ERROR,
                        "The email address or the password is incorrect"
                    )
        else:
            messages.error(request, "The form is not valid")            

    view_title = "Login"
    return render(request, 'login.html', locals())


@login_required
def logout_view(request):
    logout(request)
    messages.add_message(
        request, messages.WARNING,
        "You have been disconnected !"
    )
    return HttpResponseRedirect(reverse('home'))


def settings(request):
    pass


def home(request):
    pass