from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Material(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    year = models.ForeignKey("categories.Year", null=True, blank=True, on_delete=models.SET_NULL)


class Year(models.Model):
    year_level = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)], default=1, verbose_name="Année")
    year_name = models.CharField(max_length=50, verbose_name="Nom de l'année (Primaire/Collège/Lycée)")
