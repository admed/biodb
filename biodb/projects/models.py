from django.db import models

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100)
    create_date = models.DateField()
    description = models.TextField()

    class Meta():
        permissions = (
            ('can_visit', 'Can visit project details'),
        )