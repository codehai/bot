#coding=utf-8
from django.shortcuts import render_to_response,render,get_object_or_404,redirect    
from django.http import HttpResponse, HttpResponseRedirect    
from django.contrib.auth.models import User    
from django.contrib import auth  
from django.contrib import messages  
from django.template.context import RequestContext  
  
from django.forms.formsets import formset_factory  
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage  
  
from django.contrib.auth.decorators import login_required
from gdsou_app.models import Zixun, Races, Vipuser 

from django.contrib.auth import logout,authenticate
from .forms import RegisterForm,PasswordChangeForm,SetPasswordForm
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import FormView
from django.utils import timezone
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.template.response import TemplateResponse

def getUser(request):
    is_logged_in = request.user.is_authenticated()
    username = request.user.get_username()
    vip = {}
    if username:
        id = User.objects.get(username=username).id
        try:
            vip_obj = Vipuser.objects.get(user_id=id)
            now = timezone.now()
            vip_end = vip_obj.vip_end
            if (vip_end - now).total_seconds()>0:
                vip['status'] = True
                vip['vip_end'] = vip_end
                vip['days'] = (vip_end - now).days
            else:
                vip['status'] = False
        except Vipuser.DoesNotExist:
            vip['status'] = False
    else:
        vip['status'] = False        
    user={'username':username,'is_logged_in':is_logged_in,'vip':vip} 
    return user
  
# Create your views here.

def home(request):
    title = '鸽度搜－查信鸽成绩、足环、天落成绩、脚环！' 
    user = getUser(request)
    post_list = Zixun.objects.all()[:3]  #获取全部的Article对象
    return render(request, 'home.html', {'post_list' : post_list,'user':user, 'title':title})

def profile(request):
    title = '鸽度搜－个人设置'
    user = getUser(request)
    return render(request, 'profile.html', {'user':user, 'title':title})

def detail(request, id):
    user = getUser(request)
    try:
        post = Zixun.objects.get(id=str(id))
    except Zixun.DoesNotExist:
        raise Http404
    title = u'鸽度搜－' + post.title
    return render(request, 'post.html', {'post' : post,'user':user, 'title':title})

def zixun(request):
    user = getUser(request)
    limit = 10  # 每页显示的记录数
    post_list = Zixun.objects.all()  #获取全部的Article对象
    paginator = Paginator(post_list, limit)  # 实例化一个分页对象
    page = request.GET.get('page')  # 获取页码
    title = '鸽度搜－最新资讯'

    try:
        post_list = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        post_list = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        post_list = paginator.page(paginator.num_pages)  # 取最后一页的记录

    return render(request, 'zixun.html', {'post_list' : post_list,'user':user, 'title':title})

def race(request):
    title = '比赛成绩'
    user = getUser(request)
    q = request.GET.get('q')
    try:
        race_list = Races.objects.filter(foot_num=q)
        race_len = len(race_list)
        if not user['vip']['status']:
            race_list = race_list[0:1]
    except Races.DoesNotExist:
        race_list = []
    return render(request, 'race.html', {'title':title,'user':user,'q':q,'race_list':race_list, 'race_len':race_len})

class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(RegisterView, self).form_valid(form)

@sensitive_post_parameters()
@csrf_protect
@login_required
def password_change(request,
                    template_name='registration/password_change_form.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    current_app=None, extra_context=None):
    if post_change_redirect is None:
        post_change_redirect = reverse('password_change_done')
    else:
        post_change_redirect = resolve_url(post_change_redirect)
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Updating the password logs out all other sessions for the user
            # except the current one if
            # django.contrib.auth.middleware.SessionAuthenticationMiddleware
            # is enabled.
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
        'title': _(u'修改密码'),
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)



@login_required
def password_change_done(request,
                         template_name='registration/password_change_done.html',
                         current_app=None, extra_context=None):
    context = {
        'title': _(u'密码修改成功'),
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)



