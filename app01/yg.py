from yingun.service import v
from app01 import models
from django.urls import reverse
from django.utils.safestring import mark_safe


def func(self, obj=None,is_header=False):
    if is_header:
        return '操作'
    else:
        # str = '{0}:{1}_{2}_change'.format(self.site.namespace, self.model_class._meta.app_label,
        #                        self.model_class._meta.model_name)
        from django.http.request import QueryDict
        param_dic = QueryDict(mutable=True)
        if self.request.GET:
            param_dic['_changelistfilter'] = self.request.GET.urlencode()
        base_edit_url = reverse('{0}:{1}_{2}_change'.format(self.site.namespace, self.app_label, self.model_name),args=(obj.pk,))
        edit_url = '{0}?{1}'.format(base_edit_url, param_dic.urlencode())
        return mark_safe('<a href="{0}">编辑</a>'.format(edit_url))

def dele(self, obj=None,is_header=False):
    if is_header:
        return '操作'
    else:
        # str = '{0}:{1}_{2}_change'.format(self.site.namespace, self.model_class._meta.app_label,
        #                        self.model_class._meta.model_name)
        from django.http.request import QueryDict
        param_dic = QueryDict(mutable=True)
        if self.request.GET:
            param_dic['_changelistfilter'] = self.request.GET.urlencode()
        base_edit_url = reverse('{0}:{1}_{2}_delete'.format(self.site.namespace, self.app_label, self.model_name),args=(obj.pk,))
        edit_url = '{0}?{1}'.format(base_edit_url, param_dic.urlencode())
        return mark_safe('<a href="{0}">删除</a>'.format(edit_url))

def checkbox(self, obj=None, is_header=False):
    if is_header:
        return '筛选'
    else:
        return mark_safe('<input type="checkbox" value={0}/>'.format(obj.pk))


list_display = [checkbox, 'id', 'user', 'email', func]

class UserYinGun(v.modelYinGun):
    # def func(self,obj):
    #     print(self.model_class._meta.app_label)
    #     print(obj.pk)
    #     str= '{0}:{1}_{2}_change'.format(self.site.namespace, self.model_class._meta.app_label,
    #                                 self.model_class._meta.model_name)
    #     url = reverse(str,args=(obj.pk,))
    #     print(url)
    #     return mark_safe('<a href="{0}">编辑</a>'.format(url))
    #
    # def checkbox(self,obj):
    #     return mark_safe('<input type="checkbox" value={0}/>'.format(obj.pk))
    list_display = [checkbox,'id','user','email',func,dele]

v.site.register(models.UserInof,UserYinGun)

class RoleYinGun(v.modelYinGun):
    list_display = [checkbox,'id','name',func]

v.site.register(models.Role,RoleYinGun)

class UserGroupYinGun(v.modelYinGun):
    list_display = [checkbox,'id','title',func]
v.site.register(models.UserGroup,UserGroupYinGun)