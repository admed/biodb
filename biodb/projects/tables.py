import django_tables2 as tables
from models import RObject
import re

class CustomCheckBoxColumn(tables.CheckBoxColumn):
    ''' Custom class that inherits from tables.CheckBoxColumn and customize render method. '''

    def render(self, value, bound_column, record):
        ''' Customized render method that allow to modify all td checkbox inputs '''

        from django.utils.safestring import mark_safe
        
        # get input html string
        input_html = super(CustomCheckBoxColumn, self).render(value, bound_column, record)
        # replace previous name attr in <input/> string with 'robject_{robject.id}'
        input_html = re.sub('name=".*?"', 'name="robject_{}"'.format(record.id), input_html)
        
        return mark_safe(input_html) 

class RObjectTable(tables.Table):
    selection = CustomCheckBoxColumn(accessor='id', orderable=False, attrs={'td__input': {'class': 'select-robject', 'form': 'actions'}, 
                                                                             "th__input": {"class": "select-all"}})
    # display column with names of robjects
    name = tables.Column()
    class Meta:
        model = RObject
        attrs = {"class":"table table-hover"}
        # exclude = ["files", "tags", "author", "project"]
        fields = ["selection", "id", "name", "bio_obj", "creator", "create_date"]
        order_by = ['-id']

