from django.shortcuts import render
from .models import Survey, Question, Answer
from django.http import HttpResponse
import csv
from django.views import View

# Create your views here.
def index(request):
    surveys_list = Survey.objects.prefetch_related('questions__options').all()

    context = {
        'surveys_list': surveys_list,
    }
    return render(request, 'survey/index.html', context)


def answers(request):
    if request.method == 'POST':
        # Создаем пустой словарь для чистых ответов
        clean_answers = {}

        # Используем .lists() для итерации по всем ключам и их спискам значений
        for key, values_list in request.POST.lists():
            
            # 1. Пропускаем служебное поле csrf token
            if key == 'csrfmiddlewaretoken':
                continue

            # 2. Очищаем список значений от пустых строк ('')
            #    List comprehension [v for v in values_list if v] сделает это идеально
            processed_values = [value for value in values_list if value]

            # 3. Если после очистки в списке остались значения, добавляем их в наш словарь
            if processed_values:
                # Если значение одно (из radio или text), сохраняем как строку
                if len(processed_values) == 1:
                    clean_answers[key] = processed_values[0]
                # Если значений несколько (из checkbox), сохраняем как список
                else:
                    clean_answers[key] = processed_values

        # В `clean_answers` теперь лежат только реальные ответы
        print("Очищенные ответы:", clean_answers)

        # Здесь вы можете сохранить эти данные в базу данных или сделать что-то еще
        # ...
        for answer in clean_answers:
            question_answer = Question.objects.get(id=answer)
            option_answer = clean_answers[answer]
            Answer.objects.create(question=question_answer, option=option_answer) 

        return HttpResponse(f"Данные успешно обработаны! <br><pre>{clean_answers}</pre>")

    return HttpResponse("Это представление работает только с POST-запросами.")


class ExportAnswersCSV(View):
    def get(self, request, *args, **kwargs):
        # Создаем HTTP-ответ с указанием типа контента и заголовка
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="answers.csv"'},
        )

        # Устанавливаем кодировку UTF-8 для корректной работы с кириллицей
        response.write(u'\ufeff'.encode('utf8'))

        # Создаем "писателя" для CSV и указываем ему наш response
        writer = csv.writer(response)

        # Записываем заголовки столбцов (опционально, но рекомендуется)
        writer.writerow(['ID', 'Вопрос', 'Ответ'])

        # Получаем все объекты модели Answer и записываем их в файл
        answers = Answer.objects.all()
        for answer in answers:
            writer.writerow([answer.id, answer.question, answer.option])

        return response
