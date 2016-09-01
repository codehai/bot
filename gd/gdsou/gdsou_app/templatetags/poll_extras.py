from django import template
import datetime
from django.template.defaultfilters import stringfilter
register = template.Library()
# 以下定义自己的方法，自定义方法需要用装饰器register.filter装饰起来
@register.filter
@stringfilter
def timeformat(value):
    post_time = datetime.datetime.strptime(value,"%Y-%m-%d %H:%M:%S.%f+00:00")
    current_time = datetime.datetime.now()
    seconds = (current_time-post_time).total_seconds()
    
    if seconds<3600:
        time_str = str(seconds/60)+'分钟前'
    elif seconds>=3600 and seconds< 86400
        time_str = str(seconds/60/60)+'小时前'