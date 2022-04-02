from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

import courses.models as models


def dashboard(request):
    return render(request, 'home.html')


@login_required
def courses(request, course_id=0):
    course = get_object_or_404(models.Course, id=course_id)
    user = request.user
    return render(request, 'course.html', context={'course': course, 'user': user})
