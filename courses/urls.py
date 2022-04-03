from django.urls import path

import courses.views as views
from courses.autocomplete_view import CourseAutocomplete


urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('search', views.search, name="search"),
    path('course/<int:course_id>', views.courses, name="course"),
    path('schedule/<int:schedule_id>', views.schedule_view, name="schedule"),
    path('add_schedule', views.add_schedule, name="add_schedule"),
    path('delete_schedule/<int:id>', views.delete_schedule, name="delete_schedule"),
    path('course/rate', views.rate, name="submit_exam"),
    path('charts', views.charts, name="charts"),

    path('schedule/<int:schedule_id>/ics', views.gen_ics, name="generate_ics"),
    path('autocomplete/course', CourseAutocomplete.as_view(), name='course_autocomplete'),
]
