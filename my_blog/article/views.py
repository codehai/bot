from django.shortcuts import render
from django.http import HttpResponse
from article.models import Article
# Create your views here.

def home(request):
        return HttpResponse("Hello World, Django")

def detail(request,my_args):
        # post = Article.objects.all()[int(my_args)]
        return HttpResponse("You're looking at my_args %s." % my_args)