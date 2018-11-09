from django.template import Library
from types import FunctionType

register = Library()

def table_body(result_list,list_display,yg_admin):
    for row in  result_list:
        # yield [getattr(row,name) for name in list_display]
        yield [name(yg_admin,row) if isinstance(name,FunctionType) else getattr(row,name) for name in list_display]
def table_head(list_display):
    for item in list_display:
        # print(item.__name__ if isinstance(item,FunctionType) else item)
        yield item.__name__ if isinstance(item,FunctionType) else item

@register.inclusion_tag('yg/md.html')
def func(result_list,list_display,yg_admin):
    v = table_body(result_list,list_display,yg_admin)
    h = table_head(list_display)
    return {'xxxx':v,'hhhh':h}