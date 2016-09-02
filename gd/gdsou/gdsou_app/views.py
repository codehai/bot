from django.shortcuts import render_to_response,render,get_object_or_404    
from django.http import HttpResponse, HttpResponseRedirect    
from django.contrib.auth.models import User    
from django.contrib import auth  
from django.contrib import messages  
from django.template.context import RequestContext  
  
from django.forms.formsets import formset_factory  
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage  
  
from django.contrib.auth.decorators import login_required
from gdsou_app.models import Zixun 

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger


def getUser(request):
    is_logged_in = request.user.is_authenticated()
    username = request.user.get_username()
    user={'username':username,'is_logged_in':is_logged_in} 
    return user
  
# Create your views here.
def home(request):
    user = getUser(request)
    post_list = Zixun.objects.all()[:3]  #获取全部的Article对象
    return render(request, 'home.html', {'post_list' : post_list,'user':user})

def detail(request, id):
    user = getUser(request)
    try:
        post = Zixun.objects.get(id=str(id))
    except Zixun.DoesNotExist:
        raise Http404
    return render(request, 'post.html', {'post' : post,'user':user})

def zixun(request):
    user = getUser(request)
    limit = 3  # 每页显示的记录数
    post_list = Zixun.objects.all()  #获取全部的Article对象
    paginator = Paginator(post_list, limit)  # 实例化一个分页对象
    page = request.GET.get('page')  # 获取页码

    try:
        post_list = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        post_list = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        post_list = paginator.page(paginator.num_pages)  # 取最后一页的记录

    return render(request, 'zixun.html', {'post_list' : post_list,'user':user})

def race(request):
    user = getUser(request)
    q = request.GET.get('q')
    return render(request, 'race.html', {'user':user,'q':q})



