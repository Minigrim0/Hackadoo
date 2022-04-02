from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, reverse
import courses.models as models 
from django.http import HttpResponseRedirect, HttpResponse
from courses.utils import schedule_this
from django.contrib import messages
import users.models as umodels

import datetime


def dashboard(request):
    return render(request, 'home.html')


@login_required
def courses(request, course_id=0):
    course = get_object_or_404(models.Course, id=course_id)
    user = request.user
    return render(request, 'course.html', context={'course': course, 'user': user})


@login_required
def add_schedule(request):
    if request.method == "POST":
        form = request.POST
        user = form.get("name", "")
        study_time_per_day = datetime.time(
            hour=int(form.get("study_time_per_day_hours", 0)),
            minute=int(form.get("study_time_per_day_minutes", 0))
        )
        study_bloc_size = datetime.time(
            hour=int(form.get("pause_duration_hours", 0)),
            minute=int(form.get("pause_duration_minutes", 0))
        )
        starting_hour = datetime.time(
            hour=int(form.get("starting_hour_hours", 0)),
            minute=int(form.get("starting_hour_minutes", 0))
        )
        ending_hour = datetime.time(
            hour=int(form.get("ending_hour_hours", 0)),
            minute=int(form.get("ending_hour_minutes", 0))
        )
        pause_duration = datetime.time(
            hour=int(form.get("study_bloc_size_hours", 0)),
            minute=int(form.get("study_bloc_size_minutes", 0))
        )
        starting_date = datetime.datetime.strptime(form.get("starting_date", 0), "%Y-%m-%d").time()
        end_date = datetime.datetime.strptime(form.get("end_date", 0), "%Y-%m-%d").time()
        schedule = models.Schedule.objects.create(
            name=f"Schedule : {form.get('starting_date', 0)} to {form.get('end_date', 0)}",
            user=request.user
        )
        parameter_obj = models.Parameter.objects.create(
            schedule=schedule,
            study_time_per_day=study_time_per_day,
            study_bloc_size=study_bloc_size,
            starting_hour=starting_hour,
            ending_hour=ending_hour,
            pause_duration=pause_duration,

        )

        selected_courses = []
        s2c_qs = umodels.StudentToCourse.objects.filter(student=request.user, status="running")
        for s2c in s2c_qs:
            course = form.get(s2c.id, "")
            if course != "":
                selected_courses.append(models.Course.objects.get(id=int(course)))

        schedule_this(selected_courses, request.user, parameter_obj, starting_date, end_date)
    return HttpResponseRedirect(reverse("home"))


@login_required
def delete_schedule(request, id=0):
    models.Schedule.objects.get(id=id).delete()
    return HttpResponseRedirect(reverse("home"))

  
  
def charts(request):
    return render(request, 'charts.html', context={'user': request.user})


def rate(request):
    if request.method != "POST":
        messages.error(request,"You can only use POST for this URL")
        return HttpResponseRedirect(reverse("home"))
    data = request.POST
    course_data, _ = umodels.StudentToCourse.objects.get_or_create(student=request.user, course__id=data['course'])
    print(data)
    print(data['rating'])
    course_data.rating = data['rating']
    course_data.grade = data['grade']
    course_data.status = data['status']
    course_data.save()
    messages.success(request, "Rating saved")
    return HttpResponseRedirect(reverse("home"))
