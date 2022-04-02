from django.contrib import admin
import courses.models as models


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'faculty', 'description')
    list_filter = ('faculty',)
    search_fields = ('name', 'faculty__name')


@admin.register(models.Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(models.Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'description')
    list_filter = ('course',)
    search_fields = ('name', 'course__name')


@admin.register(models.University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'website')
    search_fields = ('name',)
