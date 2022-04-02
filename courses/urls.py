from django.urls import path

import courses.views as views


urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('course/<int:course_id>', views.courses, name="course"),
    path('add_schedule', views.add_schedule, name="add_schedule"),
    path('delete_schedule/<int:id>', views.delete_schedule, name="delete_schedule"),
]
