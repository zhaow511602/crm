from django.shortcuts import render,HttpResponse,reverse
from app01 import models
def test(request):
    obj = models.UserGroup.objects.all()
    return render(request,'test.html',{'obj':obj})



