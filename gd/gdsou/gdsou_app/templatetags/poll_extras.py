#coding=utf-8
from django import template
import datetime
import markdown2
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
        time_str = str(int(seconds/60/60/24/30)+1)+'月前'
    elif seconds>=62208000:
        time_str = str(int(seconds/60/60/24/30/12))+'月前'
    return time_str

@register.filter(is_safe=True)  #注册template filter
@stringfilter  #希望字符串作为参数
def custom_markdown(value):
    return mark_safe(markdown2.markdown(value, safe_mode=True))


@register.filter
def cut_str(str, length=21):
    """
    截取字符串，使得字符串长度等于length，并在字符串后加上省略号
    """
    is_encode = False
    try:
        str_encode = str.encode('gb18030') #为了中文和英文的长度一致（中文按长度2计算）
        is_encode = True
    except:
        pass
    if is_encode:
        l = length*2
        if l < len(str_encode):
            l = l - 3
            str_encode = str_encode[:l]
            try:
                str = str_encode.decode('gb18030') + '...'
            except:
                str_encode = str_encode[:-1]
                try:
                    str = str_encode.decode('gb18030') + '...'
                except:
                    is_encode = False
    if not is_encode:
        if length < len(str):
            length = length - 2
            return str[:length] + '...'
    return str