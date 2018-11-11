from django.template import Library
from django.forms.models import ModelChoiceField
from yingun.service import v
from django.shortcuts import reverse

register = Library()
# from django.forms.boundfield import BoundField
def editfor(form, yg_admin):
    list = []
    for item in form:
        dic = {'is_popup':False,'item':None,'popup_url':None}
        if isinstance(item.field,ModelChoiceField) and item.field.queryset.model in v.site._registry:
            dic['is_popup'] =True
            target_app_label = item.field.queryset.model._meta.app_label
            target_model_name = item.field.queryset.model._meta.model_name
            url_name = "{0}:{1}_{2}_add".format(v.site.namespace, target_app_label, target_model_name)
            target_url = "{0}?popup={1}".format(reverse(url_name), item.auto_id)
            dic['popup_url'] =target_url

        dic['name'] = item.field.label
        dic['item'] = item
        list.append(dic)
    return list


@register.inclusion_tag('yg/mdedit.html')
def func_edit(form, yg_admin):
    f = editfor(form, yg_admin)
    return {'ffff':f}