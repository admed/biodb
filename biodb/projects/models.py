from django.db import models

# Create your models here.
class Project(models.Model):
    name = models.CharField()
    create_date = models.DateField()
    description = models.TextField()