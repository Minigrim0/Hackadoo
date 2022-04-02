from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
import courses.models as models
import 

def dashboard(request):
    return render(request, 'home.html')


@login_required
def courses(request, course_id=0):
    course = get_object_or_404(models.Course, id=course_id)
    user = request.user
    return render(request, 'course.html', context={'course': course, 'user': user})

def charts(request):
    return render(request, 'charts.html', context={'user': request.user})

def rate(request):
    if request.method != "POST":
        messages.error(request,"You can only use POST for this URL")
        return HttpResponseRedirect(reverse("home"))
    data = request.POST
