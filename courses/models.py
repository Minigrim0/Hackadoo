from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Chapter(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    course = models.ForeignKey("courses.Course", verbose_name="Cours du chapitre", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    faculty = models.ForeignKey("courses.Faculty", verbose_name="Faculté du cours", on_delete=models.CASCADE)
    ects = models.PositiveIntegerField(default=0, verbose_name="ECTS")

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
