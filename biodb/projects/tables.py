import django_tables2 as tables
from models import RObject

class RObjectTable(tables.Table):
    class Meta:
        model = RObject
        attrs = {"class":"table table-hover"}
        exclude = ["files", "tags", "author", "project"]
        sequence = ["id", "bio_obj", "creator", "create_date"]

