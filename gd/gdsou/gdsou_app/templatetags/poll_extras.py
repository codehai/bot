#coding=utf-8
from django import template
import datetime
import markdown
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
register = template.Library()

@register.filter
@stringfilter
def timeformat(value):
    post_time = datetime.datetime.strptime(value,"%Y-%m-%d %H:%M:%S.%f+00:00")
    current_time = datetime.datetime.now()
    seconds = (current_time-post_time).total_seconds()
    
    if seconds<3600:
        time_str = str(int(seconds/60))+'分钟前'
    elif seconds>=3600 and seconds< 86400:
        time_str = str(int(seconds/60/60))+'小时前'
    elif seconds>=86400 and seconds< 2073600:
        time_str = str(int(seconds/60/60/24))+'天前'
    elif seconds>=2073600 and seconds<62208000:
        time_str = str(int(seconds/60/60/24/30))+'月前'
    elif seconds>=62208000:
        time_str = str(int(seconds/60/60/24/30/12))+'月前'
    return time_str

@register.filter(is_safe=True)  #注册template filter
@stringfilter  #希望字符串作为参数
def custom_markdown(value):
    return mark_safe(markdown.markdown(value,extensions = ['markdown.extensions.fenced_code', 'markdown.extensions.codehilite'],safe_mode=True,enable_attributes=False))
        