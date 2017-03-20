from django.shortcuts import render

# Create your views here.

def index(request):
    title = '傲硕科技-专注汽车领域智能语音解决方案' 
    return render(request, 'index.html', {'title':title})

def contact(request):
    title = '傲硕科技-联系我们' 
    return render(request, 'contact.html', {'title':title})
