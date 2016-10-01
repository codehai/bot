"""gdsou URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from gdsou_app import views
# from django.contrib.auth.views import login, logout
from django.contrib.auth import urls as auth_urls
from django.contrib.auth import views as auth_views 

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^login/$', views.login,name='login'),
    url(r'^accounts/register/',views.RegisterView.as_view(),name='register'),
    url(r'^accounts/', include(auth_urls,namespace='accounts')),
    url(r'^$', views.home,name='home'),
    url(r'^(?P<id>\d+)/$', views.detail, name='detail'),
    url(r'^zixun/$', views.zixun, name='zixun'),
    url(r'^race/$', views.race, name='race'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^voucher/$', views.voucher, name='contact'),
    url ( r'^password/change/$' , views.password_change , name = 'password_change' ), 
    url ( r'^password/change/done/$' , views.password_change_done , name = 'password_change_done' ), 
    url ( r'^resetpassword/$' , auth_views.password_reset , name = 'password_reset' ), 
    url ( r'^resetpassword/passwordsent/$' , auth_views.password_reset_done , name = 'password_reset_done' ), 
    url ( r'^reset/done/$' , auth_views.password_reset_complete , name = 'password_reset_complete' ), 
    url ( r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$' , auth_views.password_reset_confirm , name = 'password_reset_confirm' ), 
]
