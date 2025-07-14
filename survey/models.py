from django.db import models


class Survey(models.Model):
    """ Модель опроса. Содержит название, описание и статус. """
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Черновик'
        ACTIVE = 'ACTIVE', 'Активен'
        CLOSED = 'CLOSED', 'Закрыт'

    title = models.CharField('Название', max_length=255)
    # Связываем опрос с автором. При удалении пользователя, удалятся и все его опросы.
    status = models.CharField('Статус', max_length=10, choices=Status.choices, default=Status.DRAFT)

    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"

    def __str__(self):
        return f'"{self.title}"'
    

class Question(models.Model):
    """ Модель вопроса. Связана с конкретным опросом. """
    class Type(models.TextChoices):
        SINGLE_CHOICE = 'SINGLE', 'Одиночный выбор'
        MULTIPLE_CHOICE = 'MULTIPLE', 'Множественный выбор'
        TEXT_ANSWER = 'TEXT', 'Текстовый ответ'

    # related_name позволяет обращаться к вопросам из опроса: my_survey.questions.all()
    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField('Текст вопроса')
    type = models.CharField('Тип вопроса', max_length=10, choices=Type.choices)
    is_custom_answer = models.BooleanField('Добавить свой вариант', default=False)
    is_required = models.BooleanField('Обязательный вопрос', default=False)

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.text[:80] # Возвращаем первые 80 символов текста
    

class Option(models.Model):
    """ Модель варианта ответа для вопросов с выбором. """
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField('Текст варианта', max_length=255)

    class Meta:
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответа"

    def __str__(self):
        return self.text
    

class Answer(models.Model):
    question = models.TextField('Вопрос')
    option = models.TextField('Ответ')

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
    
    def __str__(self):
        return f"{self.id}: '{self.question[:30]}': {self.option[:30]}"