from django.shortcuts import render

# Create your views here.

def index(request):
    title = '傲硕科技！' 
    return render(request, 'index.html', {'title':title})
