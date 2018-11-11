from django.conf.urls import url,include
from django.shortcuts import render,HttpResponse,reverse,redirect
import copy

from django.contrib import admin

class modelYinGun(object):
    list_display = "__all__"
    action_list = []

    add_edit_model =None
    def __init__(self,model_class,site):
        self.model_class = model_class
        self.site = site
        self.app_label = model_class._meta.app_label
        self.model_name = model_class._meta.model_name



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

    def get_add_edit_model(self):
        if self.add_edit_model:
            return self.add_edit_model
        else:
            from django.forms import ModelForm
            # class MyModelForm(ModelForm):
            #     class Meta:
            #         model = self.model_class
            #         fields = '__all__'
            _m = type('Meta',(object,),{'model':self.model_class,'fields':'__all__'})
            MyModelForm = type('MyModelForm',(ModelForm,),{'Meta':_m})
            return MyModelForm

    def changelist_view(self,request):
        result_list = self.model_class.objects.all()
        #反向生成url
        #保留访问url数据
        from django.http.request import QueryDict
        param_dic = QueryDict(mutable=True)
        if request.GET:
            param_dic['_changelistfilter']=request.GET.urlencode()
        name = '{0}_{1}_add'.format(self.app_label, self.model_name)
        base_add_url = reverse('{0}:{1}'.format(self.site.namespace, name))
        add_url = '{0}?{1}'.format(base_add_url, param_dic.urlencode())
        self.request = request

        # ############# 分页 开始 #############
        condition = {}

        from yingun.utils.my_page import PageInfo
        all_count = self.model_class.objects.filter(**condition).count()
        base_page_url = reverse("{2}:{0}_{1}_changelist".format(self.app_label, self.model_name, self.site.namespace))
        page_param_dict = copy.deepcopy(request.GET)
        page_param_dict._mutable = True

        page_obj = PageInfo(request.GET.get('page'), all_count, base_page_url, page_param_dict,2)
        result_list = self.model_class.objects.filter(**condition)[page_obj.start:page_obj.end]
        # ############# 分页 结束 #############

        # ############# action 开始 #############
        if self.action_list:
            action_name_list = []
            for item in self.action_list:
                action_name = {'name':item.__name__,'text':item.text}
                action_name_list.append(action_name)
        else:
            action_name_list = []

        if request.method == "POST":

            action_func = request.POST.get('action')
            res = getattr(self,action_func)(request,)
            action_page_url = reverse(
                "{2}:{0}_{1}_changelist".format(self.app_label, self.model_name, self.site.namespace))
            if res:
                action_page_url = reverse(
                    "{2}:{0}_{1}_changelist".format(
                        self.app_label, self.model_name,  self.site.namespace))+'?{0}'.format(request.GET.urlencode())
            return redirect(action_page_url)
        # ############# action 结束 #############

        # ############# 组合搜索 开始 #############
        from django.db.models import ForeignKey,ManyToManyField
        from yingun.utils.filter_code import FilterList
        # if self.filter_list:
        filter_list = []
        for optin in self.filter_list:
            if optin.is_func:
                pass
            else:
                field = self.model_class._meta.get_field(optin.field_or_func)
                if isinstance(field,ForeignKey):
                    filterlist = FilterList(optin,field.rel.model.objects.all(),request)
                elif isinstance(field,ManyToManyField):
                    filterlist = FilterList(optin, field.rel.model.objects.all(),request)
                else:
                    filterlist = FilterList(optin, field.model.objects.all(), request)
            filter_list.append(filterlist)
        # ############# 组合搜索 结束 #############
        content = {
            'filter_list':filter_list,
            'list_display':self.list_display,
            'result_list':result_list,
            'yg_admin':self,
            'add_url':add_url,
            'page_obj':page_obj,
            'action_name_list':action_name_list,
        }
        return render(request,'yg/change_list.html',content)


    def add_view(self,request):

        if request.method=='GET':
            MyModelForm = self.get_add_edit_model()()
            content={
                'form': MyModelForm,
            }
            return render(request, 'yg/add.html',content)
        else:
            param_url = request.GET.get('_changelistfilter')
            MyModelForm = self.get_add_edit_model()(data=request.POST,files=request.FILES)
            if MyModelForm.is_valid():
                obj = MyModelForm.save()
                popupid = request.GET.get('popup')
                if popupid:
                    content={
                        'popupid':popupid,
                        'pk':obj.pk,
                        'text':str(obj)
                    }
                    return render(request,'yg/popup_response.html',content)
                else:
                    base_add_url = reverse('{0}:{1}_{2}_changelist'.format(self.site.namespace, self.app_label, self.model_name))
                    add_url = '{0}?{1}'.format(base_add_url, param_url)
                    return redirect(add_url)
            else:
                return HttpResponse('错误了')


    def delete_view(self,request, pk):
        obj = self.model_class.objects.filter(pk=pk).delete()
        if obj:
            param_url = request.GET.get('_changelistfilter')
            base_add_url = reverse(
                '{0}:{1}_{2}_changelist'.format(self.site.namespace, self.app_label, self.model_name))
            add_url = '{0}?{1}'.format(base_add_url, param_url)
            return redirect(add_url)
        else:
            return HttpResponse('删除失败')

    def change_view(self,request, pk):
        obj = self.model_class.objects.filter(pk=pk).first()
        if request.method =='GET':
            MyModelForm = self.get_add_edit_model()(instance=obj)
            content = {
                'form': MyModelForm,
                'yg_admin':self
            }
            return render(request, 'yg/edit.html', content)
        else:
            MyModelForm = self.get_add_edit_model()(data=request.POST,files=request.FILES,instance=obj)
            if MyModelForm.is_valid():
                MyModelForm.save()
                param_url = request.GET.get('_changelistfilter')
                base_add_url = reverse(
                    '{0}:{1}_{2}_changelist'.format(self.site.namespace, self.app_label, self.model_name))
                add_url = '{0}?{1}'.format(base_add_url, param_url)
                return redirect(add_url)
            else:
                content = {
                    'form': MyModelForm,
                }
                return render(request, 'yg/edit.html', content)



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


