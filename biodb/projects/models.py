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
    title = models.CharField()
    primary = models.CharField()

class Tag(models.Model):
    name = models.CharField()

class MoleculeFile(models.Model):
    file = models.FileField()
    description = models.RichTextField()

class BioObj(models.Model):
    ligand = models.CharField()
    receptor = models.CharField()
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
    author = models.CharField()
    creator = models.CharField()
    bio_obj = models.ForeignKey(BioObj)
    # sample = models.ForeignKey(Sample)
    notes = RichTextField()
    tags = models.ForeignKey(Tag)
    files = models.ForeignKey(MoleculeFile)
