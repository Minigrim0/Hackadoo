from django.urls import path

import courses.views as views


urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('course/<int:course_id>', views.courses, name="course"),
    path('course/rate', views.courses, name="submit_exam"),
    path('charts', views.charts, name="charts"),
]
