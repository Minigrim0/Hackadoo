from django.contrib import admin
import users.models as models

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'accountType')
    list_filter = ('accountType',)
    search_fields = ('username',)


@admin.register(models.StudentToCourse)
class StudentToCourseAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status', 'grade', 'attended', 'difficulty', 'study_time')
    list_filter = ('status',)
    search_fields = ('student', 'course')
