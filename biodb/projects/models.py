from django.db import models
from ckeditor.fields import RichTextField
from simple_history.models import HistoricalRecords
from django.contrib.auth.models import User
from watson import search as watson


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
    name = models.CharField(max_length=100)
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
    create_date = models.DateField(auto_now_add=True, null=True) # TODO: make sure aboyt auto_now_add 
    history = HistoricalRecords()
    author = models.CharField(max_length=100, null=True, blank=True)
    creator = models.ForeignKey(User, null=True)
    bio_obj = models.ForeignKey(BioObj, null=True, blank=True)
    notes = RichTextField(null=True, blank=True) 
    tags = models.ForeignKey(Tag, null=True, blank=True)
    files = models.ForeignKey(MoleculeFile, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def name(self): # method treated like attribute (cool!)
        try:
            # get related Name model with primary=True
            name = self.name_set.get(primary=True).title
        except:
            # create temporary, working title 
            name = "noname robject, created at {}, by {}".format(self.create_date, self.author)

        return name

    @staticmethod
    def get_search_fields():
        ''' Return list with fields names included in watson search (except relations) '''
        
        # exceptions handles during watson.register below
        return ["pk", "name", "author"]

            

class Name(models.Model):
    title = models.CharField(max_length=100)
    primary = models.BooleanField(blank=True)
    robject = models.ForeignKey(RObject, null=True)

    def __str__(self):
        return self.title

watson.register(RObject, fields=["creator__username", "bio_obj__name"]+RObject.get_search_fields())
watson.register(User)
watson.register(BioObj)
