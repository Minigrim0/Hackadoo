from django.contrib import admin
import users.models as models

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'accountType')
    list_filter = ('accountType',)
    search_fields = ('username',)


@admin.register(models.Parameter)
class ParameterAdmin(admin.ModelAdmin):
    list_display = ('study_time_per_day', 'study_days_per_week', 'study_bloc_size')
    search_fields = ('study_time_per_day', 'study_days_per_week', 'study_bloc_size')


@admin.register(models.StudentToCourse)
class StudentToCourseAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status', 'note', 'participation_to_the_course')
    list_filter = ('status',)
    search_fields = ('student', 'course')
