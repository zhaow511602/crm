from django.conf.urls import url,include
from django.shortcuts import render,HttpResponse

from django.contrib import admin

class modelYinGun(object):
    list_display = "__all__"
    def __init__(self,model_class,site):
        self.model_class = model_class
        self.site = site

    @property
    def urls(self):
        info = self.model_class._meta.app_label,self.model_class._meta.model_name
        urlpatterns = [
            url(r'^$', self.changelist_view, name='%s_%s_changelist' % info),
            url(r'^add/$',self.add_view, name='%s_%s_add' % info),
            url(r'^(.+)/delete/$',self.delete_view, name='%s_%s_delete' % info),
            url(r'^(.+)/change/$',self.change_view, name='%s_%s_change' % info),

        ]
        return urlpatterns

    def changelist_view(self,request):
        result_list = self.model_class.objects.all()
        content = {
            'list_display':self.list_display,
            'result_list':result_list,
            'yg_admin':self,
        }
        return render(request,'yg/change_list.html',content)

    def add_view(self,request):
        info = self.model_class._meta.app_label,self.model_class._meta.model_name
        res = '%s_%s_add' % info
        return HttpResponse(res)
    def delete_view(self,request, pk):
        info = self.model_class._meta.app_label, self.model_class._meta.model_name
        res = '%s_%s_del' % info
        return HttpResponse(res)
    def change_view(self,request, pk):
        info = self.model_class._meta.app_label, self.model_class._meta.model_name
        res = '%s_%s_change' % info
        return HttpResponse(res)



class YinGunsite(object):
    def __init__(self):
        self._registry = {}
        self.namespace = 'yingun'
        self.app_name = 'yingun'

    def register(self,model_clas, xxxx = modelYinGun):
        self._registry[model_clas] = xxxx(model_clas, self)

    def geturls(self):
        res = [
            url(r'^login/', self.login,name='login'),
            url(r'^logout/', self.logout),
        ]
        for model_clas, YinGunsite_obj in self._registry.items():
            res.append(url(r'^%s/%s/'%(model_clas._meta.app_label, model_clas._meta.model_name), include(YinGunsite_obj.urls)))
        return res
    @property
    def urls(self):
        return self.geturls(),self.app_name,self.namespace

    def login(self,requset):
        return HttpResponse('login')

    def logout(self,requset):
        return HttpResponse('logout')


site = YinGunsite()


