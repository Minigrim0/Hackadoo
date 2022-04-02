from django.urls import path

import users.views as views


urlpatterns = [
    path('login/', views.login),
    path('logout/', views.logout),
    path('settings/', views.settings),
    path('/', views.home)
]
