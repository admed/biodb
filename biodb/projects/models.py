from django.db import models
from ckeditor.fields import RichTextField
from simple_history.models import HistoricalRecords

# Create your models here.


class Project(models.Model):
    # it's slug field! letters, numbers, underscores or hyphens allowed only!
    name = models.CharField(max_length=100, null=True)
    create_date = models.DateField(null=True)
    description = models.TextField(null=True)

    class Meta():
        permissions = (
            ('can_visit_project', 'Can visit project details'),
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
    project = models.ForeignKey(Project, null=True)
    names = models.ForeignKey(Name, null=True, blank=True)
    create_date = models.DateField(null=True)
    history = HistoricalRecords()
    author = models.CharField(max_length=100, null=True)
    creator = models.CharField(max_length=100, null=True)
    bio_obj = models.ForeignKey(BioObj, null=True, blank=True)
    # sample = models.ForeignKey(Sample)
    # notes = RichTextField() # FIXME admin site problems!
    tags = models.ForeignKey(Tag, null=True, blank=True)
    files = models.ForeignKey(MoleculeFile, null=True, blank=True)

