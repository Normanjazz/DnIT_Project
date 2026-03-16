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
    

class UnitForm(forms.ModelForm):
    """
    Форма для создания/редактирования единицы измерения.
    Наследуется от ModelForm для автоматического создания полей.
    """
    
    class Meta:
        model = Unit
        fields = ['full_name', 'short_name']  # Поля, которые будут в форме
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите полное наименование (например: Метр)'
            }),
            'short_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите сокращение (например: м)'
            }),
        }
        labels = {
            'full_name': 'Полное наименование',
            'short_name': 'Сокращённое наименование',
        }
    
    def clean_full_name(self):
        """
        Валидация уникальности полного наименования.
        Проверяет, что нет другой единицы измерения с таким же именем.
        """
        full_name = self.cleaned_data.get('full_name')
        
        # Если редактируем существующий объект, исключаем его из проверки
        if self.instance.pk:
            exists = Unit.objects.filter(
                full_name__iexact=full_name
            ).exclude(pk=self.instance.pk).exists()
        else:
            # Если создаём новый, проверяем все записи
            exists = Unit.objects.filter(
                full_name__iexact=full_name
            ).exists()
        
        if exists:
            raise forms.ValidationError('Единица измерения с таким наименованием уже существует.')
        
        return full_name
    

class CounterpartyForm(forms.ModelForm):
    """
    Форма для создания/редактирования контрагента.
    Наследуется от ModelForm для автоматического создания полей.
    """
    
    class Meta:
        model = Counterparty
        fields = ['name', 'inn', 'kpp', 'address', 'email', 'phone']  # Все поля модели
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите полное наименование организации'
            }),
            'inn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '10 или 12 цифр',
                'maxlength': '12'
            }),
            'kpp': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '9 символов (при наличии)',
                'maxlength': '15'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите юридический адрес',
                'rows': 3
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@domain.ru'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (XXX) XXX-XX-XX'
            }),
        }
        labels = {
            'name': 'Наименование организации',
            'inn': 'ИНН',
            'kpp': 'КПП',
            'address': 'Юридический адрес',
            'email': 'E-mail',
            'phone': 'Телефон',
        }
    
    def clean_name(self):
        """
        Валидация уникальности наименования контрагента.
        """
        name = self.cleaned_data.get('name')
        
        if self.instance.pk:
            exists = Counterparty.objects.filter(
                name__iexact=name
            ).exclude(pk=self.instance.pk).exists()
        else:
            exists = Counterparty.objects.filter(
                name__iexact=name
            ).exists()
        
        if exists:
            raise forms.ValidationError('Контрагент с таким наименованием уже существует.')
        
        return name
    
    def clean_inn(self):
        """
        Валидация ИНН: 10 цифр (ЮЛ) или 12 цифр (ИП), либо пусто.
        """
        inn = self.cleaned_data.get('inn')
        
        # Если поле пустое — возвращаем пустую строку (blank=True разрешает)
        if not inn:
            return ''
        
        # Удаляем все нецифровые символы
        inn = ''.join(c for c in inn if c.isdigit())
        
        # Проверяем длину
        if len(inn) not in [10, 12]:
            raise forms.ValidationError('ИНН должен содержать 10 или 12 цифр.')
        
        return inn
    
    def clean_kpp(self):
        """
        Валидация КПП: 9 символов, либо пусто.
        """
        kpp = self.cleaned_data.get('kpp')
        
        # Если поле пустое — возвращаем пустую строку
        if not kpp:
            return ''
        
        # Проверяем длину
        if len(kpp) not in [9, 15]:
            raise forms.ValidationError('КПП должен содержать 9 или 15 символов.')
        
        return kpp