from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.
class User(AbstractUser):
    user_types = (
        ('admin', 'Admin'),
        ('prof', 'Professor'),
        ('student', 'Student'),
    )

    accountType = models.CharField(choices=user_types, default="student", blank=False, max_length=10)
    courses = models.ManyToManyField("courses.Course", verbose_name="Follows")

    parameters = models.OneToOneField("users.Parameter", verbose_name="parametre d'étude", on_delete=models.CASCADE)
    courses = models.ManyToManyField("courses.Course", verbose_name="Cours suivits", through="users.StudentCourse")


class Parameter(models.Model):
    study_time_per_day = models.PositiveIntegerField(default=0, verbose_name="Temps d'étude par jour")
    study_days_per_week = models.PositiveIntegerField(default=0, verbose_name="Jours d'étude par semaine")
    study_bloc_size = models.PositiveIntegerField(default=0, verbose_name="Taille d'un bloc d'étude")


class StudentToCourse(models.Model):

    status_choices = (
        ('running', 'En cours'),
        ('succeeded', 'Réussi'),
        ('failed', 'Raté'),
    )

    student = models.ForeignKey("users.User", verbose_name="Etudiant", on_delete=models.CASCADE)
    course = models.ForeignKey("courses.Course", verbose_name="Cours", on_delete=models.CASCADE)
    status = models.CharField(choices=status_choices, max_length=10, default="running")
    note = models.PositiveIntegerField(default=0, verbose_name="Note")
    participation_to_the_course = models.BooleanField("A participé au cours", default=False)