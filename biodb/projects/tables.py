import django_tables2 as tables
from models import RObject
import re

class CustomCheckBoxColumn(tables.CheckBoxColumn):
    ''' Custom class that inherits from tables.CheckBoxColumn and customize render method. '''

    def render(self, value, bound_column, record):
        ''' Customized render method that allow to replace name attr in all td checkbox inputs '''

        from django.utils.safestring import mark_safe
        
        input_html = super(CustomCheckBoxColumn, self).render(value, bound_column, record)
        # replace previous name attr value with record.id (robject.id in fact)
        input_html = re.sub('name=".*?"', 'name="{}"'.format(record.id), input_html)
        
        return mark_safe(input_html) 

class RObjectTable(tables.Table):
    selection = CustomCheckBoxColumn(accessor='id', orderable=False, attrs={'td__input': {'class': 'select-robject', 'form': 'id_action_posts', 'onchange': 'actionCounter();', 'value':'none'}, 
                                                                             "th__input": {"class": "select-all"}})
    class Meta:
        model = RObject
        attrs = {"class":"table table-hover"}
        exclude = ["files", "tags", "author", "project"]
        sequence = ["selection", "id", "bio_obj", "creator", "create_date"]
        order_by = ['-id']
