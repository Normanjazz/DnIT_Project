# apps/directories/forms.py
from django import forms
from .models import WorkType, Unit, Counterparty, Contract, ResponsiblePerson, PowerOfAttorney


class WorkTypeForm(forms.ModelForm):
    """
    Форма для создания/редактирования вида работ.
    Наследуется от ModelForm для автоматического создания полей.
    """
    
    class Meta:
        model = WorkType
        fields = ['full_name', 'short_name']  # Поля, которые будут в форме
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите полное наименование вида работ'
            }),
            'short_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите сокращённое наименование'
            }),
        }
        labels = {
            'full_name': 'Полное наименование',
            'short_name': 'Сокращённое наименование',
        }
    
    def clean_full_name(self):
        """
        Валидация уникальности полного наименования.
        Проверяет, что нет другого вида работ с таким же именем.
        """
        full_name = self.cleaned_data.get('full_name')
        
        # Если редактируем существующий объект, исключаем его из проверки
        # __iexact - Регистронезависимое сравнение строк (Работ = РАБОТ)
        if self.instance.pk:
            exists = WorkType.objects.filter(
                full_name__iexact=full_name
            ).exclude(pk=self.instance.pk).exists()
        else:
            # Если создаём новый, проверяем все записи
            exists = WorkType.objects.filter(
                full_name__iexact=full_name
            ).exists()
        
        if exists:
            # ValidationError - Ошибка валидации, которая отображается пользователю
            raise forms.ValidationError('Вид работ с таким наименованием уже существует.')
        
        return full_name