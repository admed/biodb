from django.db import models
from ckeditor.fields import RichTextField
from simple_history.models import HistoricalRecords

# Create your models here.
class Project(models.Model):
    # slug field!
    name = models.CharField(max_length=100, null=True)
    create_date = models.DateField(null=True)
    description = models.TextField(null=True)

    class Meta():
        permissions = (
            ('can_visit', 'Can visit project details'),
        )

    def __str__(self):
        return self.name

class Name(models.Model):
    title = models.CharField(max_length=100)
    primary = models.CharField(max_length=100)

class Tag(models.Model):
    name = models.CharField(max_length=100)

class MoleculeFile(models.Model):
    file = models.FileField()
    description = RichTextField()

class BioObj(models.Model):
    ligand = models.CharField(max_length=100)
    receptor = models.CharField(max_length=100)
    ref_seq = RichTextField()
    mod_seq = RichTextField()
    description = RichTextField()
    bibliography = RichTextField()
    ref_commercial = RichTextField()
    ref_clinical = RichTextField()

class RObject(models.Model):
    names = models.ForeignKey(Name)
    create_date = models.DateField()
    history = HistoricalRecords()
    author = models.CharField(max_length=100)
    creator = models.CharField(max_length=100)
    bio_obj = models.ForeignKey(BioObj)
    # sample = models.ForeignKey(Sample)
    notes = RichTextField()
    tags = models.ForeignKey(Tag)
    files = models.ForeignKey(MoleculeFile)
