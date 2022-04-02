from django.urls import path

import courses.views as views


urlpatterns = [
    path('/', views.dashboard, name="dashboard"),
]
