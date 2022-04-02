from django.contrib import admin
import users.models as models

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'accountType')
    list_filter = ('accountType',)
    search_fields = ('username',)


@admin.register(models.StudentToCourse)
class StudentToCourseAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status', 'grade', 'participation_to_the_course', 'difficulty')
    list_filter = ('status',)
    search_fields = ('student', 'course')
