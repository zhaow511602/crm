import copy
from types import FunctionType
from django.utils.safestring import mark_safe
class FilterOption(object):
    def __init__(self, field_or_func, is_multi=False, text_func_name=None, val_func_name=None):
        """
        :param field: 字段名称或函数
        :param is_multi: 是否支持多选
        :param text_func_name: 在Model中定义函数，显示文本名称，默认使用 str(对象)
        :param val_func_name:  在Model中定义函数，显示文本名称，默认使用 对象.pk
        """
        self.field_or_func = field_or_func
        self.is_multi = is_multi
        self.text_func_name = text_func_name
        self.val_func_name = val_func_name

    @property
    def is_func(self):
        if isinstance(self.field_or_func, FunctionType):
            return True

    @property
    def name(self):
        if self.is_func:
            return self.field_or_func.__name__
        else:
            return self.field_or_func

class FilterList(object):
    def __init__(self,option,queryset,request):
        self.option = option
        self.queryset = queryset
        self.param_dict = copy.deepcopy(request.GET)
        self.path_info = request.path_info

    def __iter__(self):
        yield mark_safe("<div class='all-area'>")
        #全部
        if self.option.name in self.param_dict:
            pop = self.param_dict.pop(self.option.name)
            url = '{0}?{1}'.format(self.path_info,self.param_dict.urlencode())
            self.param_dict.setlist(self.option.name, pop)
            yield mark_safe('<a href="{0}">全部</a>'.format(url))
        else:
            url = '{0}?{1}'.format(self.path_info, self.param_dict.urlencode())
            yield mark_safe('<a class="active" href="{0}">全部</a>'.format(url))

        yield mark_safe("</div><div class='others-area'>")
        #筛选内容
        for row in self.queryset:
            param_dict = copy.deepcopy(self.param_dict)
            print(type(row))
            #text
            text = getattr(row,self.option.text_func_name)() if self.option.text_func_name else str(row)
            #val
            val = str(getattr(row, self.option.val_func_name)() if self.option.val_func_name else row.pk)
            #多选
            tag = False
            if self.option.is_multi:
                #pk在不在多选里面
                action_list = self.param_dict.getlist(self.option.name)
                if val in action_list:
                    action_list.remove(val)
                    tag = True
                else:
                    param_dict.appendlist(self.option.name,val)

            #单选
            else:
                action_list = self.param_dict.getlist(self.option.name)
                if val in action_list:
                    tag = True
                param_dict[self.option.name] = val

            url = '{0}?{1}'.format(self.path_info, param_dict.urlencode())
            if tag:
               tyl = "<a class='active' href='{0}'>{1}</a>".format(url,text)
            else:
                tyl ="<a href='{0}'>{1}</a>".format(url, text)
            yield mark_safe(tyl)

        yield mark_safe("</div>")




