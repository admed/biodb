from django.db import models

# Create your models here.


class Project(models.Model):
    # it's slug field! letters, numbers, underscores or hyphens allowed only!
    name = models.CharField(max_length=100, null=True)
    create_date = models.DateField(null=True)
    description = models.TextField(null=True)

    class Meta():
        permissions = (
            ('can_visit', 'Can visit project details'),
        )

    def __str__(self):
        return self.name
