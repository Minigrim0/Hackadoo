from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from courses.models import Schedule
from users.models import StudentToCourse


@login_required
def home(request):
    user = request.user
    schedules = Schedule.objects.filter(user=user)
    s2c_qs = StudentToCourse.objects.filter(student=user, status="running")
    return render(request, 'index.html', context={'user': user, "schedules": schedules, "s2c_qs": s2c_qs})
