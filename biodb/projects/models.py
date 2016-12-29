from django.db import models
from ckeditor.fields import RichTextField
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User

# Create your models here.


class Project(models.Model):
    # it's slug field! letters, numbers, underscores or hyphens allowed only!
    # TODO: consider using SlugField in this model and set on autopopulate (docs) 
    name = models.CharField(max_length=100, null=True)
    create_date = models.DateField(null=True)
    description = models.TextField(null=True)

    class Meta():
        permissions = (
            ('can_visit_project', 'Can visit project details'),
        )

    def __str__(self):
        return self.name


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
    create_date = models.DateField(null=True)
    history = HistoricalRecords()
    author = models.CharField(max_length=100, null=True)
    creator = models.ForeignKey(User, null=True)
    bio_obj = models.ForeignKey(BioObj, null=True, blank=True)
    # notes = RichTextField() # FIXME admin site problems!
    tags = models.ForeignKey(Tag, null=True, blank=True)
    files = models.ForeignKey(MoleculeFile, null=True, blank=True)

    def __str__(self):
        if not self.name_set.all():
            # create temporary, working title 
            return "noname robject, created at {}, by {}".format(self.create_date, self.author)
        else:
            # get related Name model with primary=True
            name = self.name_set.all().get(primary=True)
            return name.title
            

class Name(models.Model):
    title = models.CharField(max_length=100)
    primary = models.BooleanField(blank=True)
    robject = models.ForeignKey(RObject, null=True)
