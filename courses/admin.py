from django.contrib import admin
import courses.models as models


class BlockInline(admin.TabularInline):
    model = models.Block
    extra = 0


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'faculty', 'description')
    list_filter = ('faculty',)
    search_fields = ('name', 'faculty__name')


@admin.register(models.Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(models.University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'website')
    search_fields = ('name',)


@admin.register(models.TimeTable)
class TimeTableAdmin(admin.ModelAdmin):
    list_display = ('day', 'start_hour', 'end_hour')
    search_fields = ('day',)


@admin.register(models.Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ('time_table', 'bloc_type', 'course', 'index', 'size')
    search_fields = ('time_table', 'bloc_type', 'course')


@admin.register(models.Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name', 'user__username',)

    inlines = [
        BlockInline,
    ]

@admin.register(models.Parameter)
class ParameterAdmin(admin.ModelAdmin):
    list_display = ('id', 'schedule')
    search_fields = ('schedule__user__username',)
