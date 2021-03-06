from django.db import models
from django.shortcuts import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import StudentToCourse
import math
from datetime import datetime, timedelta

class Course(models.Model):
    class_choices = (
        ('course_1', 'course_1'),
        ('course_2', 'course_2'),
        ('course_3', 'course_3'),
        ('course_4', 'course_4'),
        ('course_5', 'course_5'),
    )

    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    faculty = models.ForeignKey("courses.Faculty", verbose_name="Faculté du cours", on_delete=models.CASCADE)
    ects = models.PositiveIntegerField(default=0, verbose_name="ECTS")
    course_class = models.CharField(max_length=8, choices=class_choices, default='course_1')

    @property
    def avg_grade(self):
        s2c_qs = self.studenttocourse_set.all()
        grades = s2c_qs.values_list('grade')
        grades = [x[0] for x in grades]
        return round(sum(grades) / len(grades), 2)
    
    @property
    def avg_difficulty(self):
        s2c_qs = self.studenttocourse_set.all()
        difficulty = s2c_qs.values_list('difficulty')
        difficulty = [x[0] for x in difficulty]
        return round(sum(difficulty) / len(difficulty), 2)
    @property
    def avg_study_time(self):
        s2c_qs = self.studenttocourse_set.all()
        study_time = s2c_qs.values_list('study_time')
        study_time = [x[0] for x in study_time]
        return round(sum(study_time) / len(study_time), 2)

    @property
    def avg_stars(self):
        return round(self.avg_difficulty/2, 2)
    
    @property
    def real_ects(self):
        return math.ceil(self.avg_study_time / 25)

    def __str__(self):
        return self.name


class Faculty(models.Model):
    name = models.CharField(max_length=200)
    university = models.ForeignKey("courses.University", verbose_name="Université de la fac", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class University(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    website = models.CharField(default="example.com", max_length=100)

    def __str__(self):
        return self.name

class TimeTable(models.Model):
    day = models.DateField("date", auto_now=False, auto_now_add=False)
    start_hour = models.TimeField(default="08:00:00")
    end_hour = models.TimeField(default="09:00:00")

    def __str__(self):
        return str(self.day) + " " + str(self.start_hour) + "-" + str(self.end_hour)


class Block(models.Model):
    bloc_types = (
        ('study', "Étude"),
        ('pause', "Pause"),
    )

    time_table = models.ForeignKey("courses.TimeTable", verbose_name="Horaire", on_delete=models.CASCADE)
    bloc_type = models.CharField(choices=bloc_types, max_length=5)
    course = models.ForeignKey("courses.Course", null=True, blank=True, verbose_name="Cours", on_delete=models.CASCADE)
    schedule = models.ForeignKey("courses.Schedule", verbose_name="Planning", on_delete=models.CASCADE)

    @property
    def index(self):
        return self.time_table.start_hour.hour * 4 + self.time_table.start_hour.minute // 15

    @property
    def end_index(self):
        return self.time_table.end_hour.hour * 4 + self.time_table.end_hour.minute // 15

    @property
    def size(self):
        return (self.end_index - self.index)

    @property
    def day_of_week(self):
        days = [
            "Monday", "Tuesday", "Wednesday",
            "Thursday", "Friday", "Saturday", "Sunday"]
        return days[self.time_table.day.weekday()]


class Schedule(models.Model):
    name = models.CharField(max_length=200, default="Planning de ouf fréro")
    user = models.ForeignKey("users.User", verbose_name="Utilisateur du schedule", on_delete=models.CASCADE)

    @property
    def start_date(self):
        if len(self.block_set.all()) == 0:
            return "AGADIDADO"
        return self.block_set.all().order_by("time_table__day", "time_table__start_hour").first().time_table.day 
    
    @property
    def end_date(self):
        if len(self.block_set.all()) == 0:
            return "AGADIDADO"
        return self.block_set.all().order_by("time_table__day", "time_table__start_hour").last().time_table.day

    @property
    def this_week(self):
        today = datetime.today()
        start_of_week = today - timedelta(days=today.weekday())  # Monday
        end_of_week = start_of_week + timedelta(days=6)  # Sunday

        return self.block_set.filter(time_table__day__gte=start_of_week, time_table__day__lte=end_of_week)

    @property
    def url(self):
        return reverse("schedule", kwargs={"schedule_id": self.id})


class Parameter(models.Model):
    schedule = models.OneToOneField("courses.Schedule", verbose_name="schedule de l'object parametres", on_delete=models.CASCADE)

    study_time_per_day = models.TimeField(default="08:00:00", verbose_name="Temps d'étude par jour")
    study_days_per_week = models.PositiveIntegerField(default=7, verbose_name="Jours d'étude par semaine")
    study_bloc_size = models.TimeField(default="08:00:00", verbose_name="Taille d'un bloc d'étude")
    starting_hour = models.TimeField(default="08:00:00")
    ending_hour = models.TimeField(default="18:00:00")
    pause_duration = models.TimeField(default="00:30:00", verbose_name="Durée de la pause")
