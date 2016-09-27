#coding=utf-8
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Zixun(models.Model) :
    title = models.CharField(max_length = 100)  #博客题目
    category = models.CharField(max_length = 50, blank = True)  #博客标签
    date_time = models.DateTimeField(auto_now_add = True)  #博客日期
    content = models.TextField(blank = True, null = True)  #博客文章正文

    #python2使用__unicode__, python3使用__str__
    def __unicode__(self) :
        return self.title

    class Meta:  #按时间下降排序
        ordering = ['-date_time']

class Vipuser(models.Model):
    user = models.OneToOneField(User)
    vip_start = models.DateTimeField(auto_now_add = False)
    vip_end = models.DateTimeField(auto_now_add = False)

class Races(models.Model):
    score = models.IntegerField()
    release_date = models.DateTimeField()
    belong = models.CharField(max_length = 50)
    return_date = models.DateTimeField()
    velocity = models.FloatField()
    distance = models.FloatField()
    company = models.CharField(max_length = 50)
    foot_num = models.CharField(max_length = 50)
    shed_num = models.IntegerField()
    race_name = models.CharField(max_length = 100)

    def __unicode__(self) :
        return self.foot_num


