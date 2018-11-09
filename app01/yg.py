from yingun.service import v
from app01 import models
from django.urls import reverse
from django.utils.safestring import mark_safe


def func(self, obj):
    print(self.model_class._meta.app_label)
    print(obj.pk)
    str = '{0}:{1}_{2}_change'.format(self.site.namespace, self.model_class._meta.app_label,
                                      self.model_class._meta.model_name)
    url = reverse(str, args=(obj.pk,))
    print(url)
    return mark_safe('<a href="{0}">编辑</a>'.format(url))


def checkbox(self, obj):
    return mark_safe('<input type="checkbox" value={0}/>'.format(obj.pk))


list_display = [checkbox, 'id', 'user', 'email', func]

class UserYinGun(v.modelYinGun):
    def func(self,obj):
        print(self.model_class._meta.app_label)
        print(obj.pk)
        str= '{0}:{1}_{2}_change'.format(self.site.namespace, self.model_class._meta.app_label,
                                    self.model_class._meta.model_name)
        url = reverse(str,args=(obj.pk,))
        print(url)
        return mark_safe('<a href="{0}">编辑</a>'.format(url))

    def checkbox(self,obj):
        return mark_safe('<input type="checkbox" value={0}/>'.format(obj.pk))
    list_display = [checkbox,'id','user','email',func]

v.site.register(models.UserInof,UserYinGun)

class RoleYinGun(v.modelYinGun):
    list_display = [checkbox,'id','name',func]

v.site.register(models.Role,RoleYinGun)
