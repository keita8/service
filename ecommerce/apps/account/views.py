from django.shortcuts import render

# Create your views here.
def index(request):
    template_name = 'layout/index.html'
    context = {}
    return render(request, template_name, context)
    