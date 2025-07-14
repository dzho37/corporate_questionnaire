from django.shortcuts import render
from .models import Survey

# Create your views here.
def index(request):
    surveys_list = Survey.objects.prefetch_related('questions__options').all()
    context = {
        'surveys_list': surveys_list
    }
    return render(request, 'survey/index.html', context)