from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, reverse
import courses.models as models
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from courses.utils import schedule_this
from django.contrib import messages
import users.models as umodels
import json
import datetime
import io

from wsgiref.util import FileWrapper
from ics import Calendar, Event


@login_required
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
        pause_duration = datetime.time(
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
        study_bloc_size = datetime.time(
            hour=int(form.get("study_bloc_size_hours", 0)),
            minute=int(form.get("study_bloc_size_minutes", 0))
        )
        starting_date = datetime.datetime.strptime(form.get("starting_date", 0), "%Y-%m-%d")
        end_date = datetime.datetime.strptime(form.get("end_date", 0), "%Y-%m-%d").replace(hour=23, minute=59)
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
            course = form.get(str(s2c.course.id), "")
            if course != "":
                selected_courses.append(s2c.course)

        print(selected_courses)
        days = schedule_this(selected_courses, request.user, parameter_obj, starting_date, end_date)
        current_date = starting_date
        for day in days:
            current_date = current_date.replace(hour=parameter_obj.starting_hour.hour, minute=parameter_obj.starting_hour.minute)

            for course_block in day:
                # Study bloc
                time_table = models.TimeTable.objects.create(
                    day=current_date,
                    start_hour=datetime.time(hour=current_date.hour, minute=current_date.minute),
                    end_hour=(current_date + datetime.timedelta(hours=parameter_obj.study_bloc_size.hour, minutes=parameter_obj.study_bloc_size.minute)).time(),
                )
                block = models.Block.objects.create(
                    schedule=schedule,
                    time_table=time_table,
                    course=course_block[0],
                    bloc_type="study"
                )
                current_date += datetime.timedelta(hours=parameter_obj.study_bloc_size.hour, minutes=parameter_obj.study_bloc_size.minute)

                if day.index(course_block) < len(day) - 1:
                    # Pause Bloc
                    pause_time_table = models.TimeTable.objects.create(
                        day=current_date,
                        start_hour=datetime.time(hour=current_date.hour, minute=current_date.minute),
                        end_hour=(current_date + datetime.timedelta(hours=parameter_obj.pause_duration.hour, minutes=parameter_obj.pause_duration.minute)).time(),
                    )
                    block = models.Block.objects.create(
                        schedule=schedule,
                        time_table=pause_time_table,
                        bloc_type="pause"
                    )
                current_date += datetime.timedelta(hours=parameter_obj.pause_duration.hour, minutes=parameter_obj.pause_duration.minute)

            current_date += datetime.timedelta(days=1)

    return HttpResponseRedirect(reverse("home"))


@login_required
def delete_schedule(request, id=0):
    models.Schedule.objects.get(id=id).delete()
    return HttpResponseRedirect(reverse("home"))


@login_required
def gen_ics(request, schedule_id=0):
    schedule = get_object_or_404(models.Schedule, id=schedule_id)
    calendar = Calendar()
    for block in schedule.block_set.all():
        event = Event()
        if block.bloc_type == "pause":
            event.name = "Break"
        else:
            event.name = block.course.name
        event.begin = datetime.datetime.combine(block.time_table.day, block.time_table.start_hour)
        event.end = datetime.datetime.combine(block.time_table.day, block.time_table.end_hour)
        calendar.events.add(event)

    ics_file = io.StringIO(str(calendar))

    response = HttpResponse(FileWrapper(ics_file), content_type="text/ics")
    response['Content-disposition'] = f"attachment; filename={schedule.name}.ics"
    return response


@login_required
def search(request):
    query = request.GET.get("q", "")
    course_list = models.Course.objects.filter(name__icontains=query)
    return render(request, 'course_list.html', context={'course_list': course_list})


def schedule_view(request, schedule_id=0):
    schedule = get_object_or_404(models.Schedule, id=schedule_id)
    return render(request, 'schedule.html', context={'schedule': schedule, 'user': request.user})


@login_required
def charts(request):
    courses_qs = list(umodels.StudentToCourse.objects.filter(student=request.user, status="running"))
    courses = sorted(courses_qs, key=lambda x: x.course.avg_grade, reverse=True)    
    avg_grades = [course.course.avg_grade for course in courses]
    names = [course.course.name for course in courses]
    names = json.dumps(names)
    avg_grades = json.dumps(avg_grades)
    courses = sorted(courses_qs, key=lambda x: x.course.avg_difficulty, reverse=True)  
    avg_difficulty = [course.course.avg_difficulty for course in courses]
    names_difficulty = [course.course.name for course in courses]
    avg_difficulty = json.dumps(avg_difficulty)
    names_difficulty = json.dumps(names_difficulty)

    courses = sorted(courses_qs, key=lambda x: x.course.avg_study_time, reverse=True)  
    avg_study_time = [course.course.avg_study_time for course in courses]
    names_study_time = [course.course.name for course in courses]
    avg_study_time = json.dumps(avg_study_time)
    names_study_time = json.dumps(names_study_time)    
    return render(request, 'charts.html', context={
        'user': request.user,
        "courses": names,
        "avg_grades": avg_grades,
        "avg_difficulty": avg_difficulty,
        "courses_difficulty": names_difficulty,
        "avg_study_time": avg_study_time, 
        "names_study_time": names_study_time, 
        })


@login_required
def rate(request):
    if request.method != "POST":
        messages.error(request,"You can only use POST for this URL")
        return HttpResponseRedirect(reverse("home"))
    data = request.POST
    course_data, _ = umodels.StudentToCourse.objects.get_or_create(student=request.user, course__id=data['course'])

    course_data.difficulty = data['rating']
    course_data.grade = data['grade']
    course_data.status = data['status']
    course_data.attended = True if data.get("attended", "") == "on" else False
    course_data.save()
    messages.success(request, "Rating saved")
    return HttpResponseRedirect(reverse("home"))
