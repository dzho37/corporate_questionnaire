from django.urls import path
from . import views
from .views import ExportAnswersCSV


urlpatterns = [
    path('', views.index, name='index'),
    path('answers', views.answers, name='answers'),
    path('export-answers-csv/', ExportAnswersCSV.as_view(), name='export_answers_csv')
]