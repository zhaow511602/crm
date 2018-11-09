from django.shortcuts import render,HttpResponse,reverse

def test(request):
    url = reverse('yingun:login')
    print(url)
    return HttpResponse('..')
