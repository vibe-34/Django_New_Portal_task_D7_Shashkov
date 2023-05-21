from django import forms
from .models import Record
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea


class RecordForm(ModelForm):
    full_text = forms.CharField(min_length=20,
                                widget=forms.Textarea
                                (attrs={'class': 'form-control', 'placeholder': 'Текст публикации'}))

    def __init__(self, *args, **kwargs):
        """Конструктор позволяет заменить свойство empty_label для поля category """
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Категория не выбрана'

    class Meta:                                              # в нем укажем характеристики
        model = Record                                       # модель с которой будем работать
        fields = ['title', 'full_text', 'data', 'category']  # создадим список полей

        widgets = {
            'title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Название публикации'}),
            'data': DateTimeInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Дата публикации'}),
            # 'full_text': Textarea(attrs={'class': 'form-control', 'placeholder': 'Текст публикации'}),
            # 'category__title': TextInput(attrs={'class': 'form-control', 'placeholder': 'Категория'})
        }
