from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import StudentToCourse

class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    faculty = models.ForeignKey("courses.Faculty", verbose_name="Faculté du cours", on_delete=models.CASCADE)
    ects = models.PositiveIntegerField(default=0, verbose_name="ECTS")
    course_color = models.CharField(max_length=7, default="#000000")

    @property
    def avg_grade(self):
        s2c_qs = self.studenttocourse_set.all()
        grades = s2c_qs.values_list('grade').first()
        return round(sum(grades) / len(grades), 2)
    
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
    course = models.ForeignKey("courses.Course", null=True, verbose_name="Cours", on_delete=models.CASCADE)
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
    


class Parameter(models.Model):
    schedule = models.OneToOneField("courses.Schedule", verbose_name="schedule de l'object parametres", on_delete=models.CASCADE)

    study_time_per_day = models.TimeField(default="08:00:00", verbose_name="Temps d'étude par jour")
    study_days_per_week = models.PositiveIntegerField(default=7, verbose_name="Jours d'étude par semaine")
    study_bloc_size = models.TimeField(default="08:00:00", verbose_name="Taille d'un bloc d'étude")
    starting_hour = models.TimeField(default="08:00:00")
    ending_hour = models.TimeField(default="18:00:00")
    pause_duration = models.TimeField(default="00:30:00", verbose_name="Durée de la pause")
