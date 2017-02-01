import django_tables2 as tables
from django_tables2.utils import A
from models import RObject
from bs4 import BeautifulSoup

class CustomCheckBoxColumn(tables.CheckBoxColumn):
    ''' Custom class that inherits from tables.CheckBoxColumn and customize render method. '''

    def render(self, value, bound_column, record):
        ''' Customized CheckBoxColumn.render() method: allow to modify checkbox inputs name attr in table's <td> 
        (ugly way but attrs kwarg in CheckBoxColumn not working in this case) '''

        from django.utils.safestring import mark_safe
        
        # get input html string
        input_html = super(CustomCheckBoxColumn, self).render(value, bound_column, record)
        
        # modify input name
        input_html = self.modify_input_name(input_html, record) 

        return mark_safe(input_html)

    @staticmethod
    def modify_input_name(input_html, record):
        ''' Change name attr in input using beautiful soup and table record (row) data '''  
        
        # get soup
        soup = BeautifulSoup(input_html, 'html.parser')
        # get tag
        tag = soup.input
        # change name
        tag["name"] = "{}".format(record.id)
        return str(tag)

class RObjectTable(tables.Table):
    selection = CustomCheckBoxColumn(accessor='id', orderable=False, attrs={'td__input': {'class': 'select-robject', 'form': 'actions-form', 'value':'check'}, 
                                                                             "th__input": {"class": "select-all"}})
    # display column with names of robjects (link to details)
    name = tables.LinkColumn('projects:robject_detail', args=[A('project.name'), A('pk')])
    class Meta:
        model = RObject
        attrs = {"class":"table table-hover"}
        # exclude = ["files", "tags", "author", "project"]
        fields = ["selection", "id", "name", "bio_obj", "creator", "create_date"]
        order_by = ['-id']