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
    

class ContractForm(forms.ModelForm):
    """
    Форма для создания/редактирования договора.
    Наследуется от ModelForm для автоматического создания полей.
    
    ВАЖНО: Counterparty выбирается через модальное окно (HTMX),
    а не через стандартный Select.
    """
    
    # Поле для отображения названия контрагента (readonly)
    counterparty_display = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly',
            'placeholder': 'Нажмите "Выбрать" для поиска контрагента'
        }),
        label="Контрагент"
    )
    
    class Meta:
        model = Contract
        fields = ['number', 'date', 'counterparty']  # counterparty - скрытое поле
        widgets = {
            'number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите номер договора (например: 12-А)'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'  # HTML5 date picker
            }),
            # СКРЫТОЕ ПОЛЕ для ID контрагента
            'counterparty': forms.HiddenInput(attrs={
                'id': 'counterparty-id'  # Важно для JavaScript
            }),
        }
        labels = {
            'number': 'Номер договора',
            'date': 'Дата договора',
            'counterparty': 'Контрагент',
        }
    
    def __init__(self, *args, **kwargs):
        """
        Инициализация формы.
        Заполняем counterparty_display текущим значением при редактировании.
        """
        super().__init__(*args, **kwargs)
        
        # Если редактируем существующий объект, заполняем отображаемое поле
        if self.instance.pk and self.instance.counterparty:
            self.fields['counterparty_display'].initial = self.instance.counterparty.name
    
    def clean(self):
        """
        Кросс-полевая валидация уникальности пары номер+дата.
        """
        cleaned_data = super().clean()
        number = cleaned_data.get('number')
        date = cleaned_data.get('date')
        
        # Если есть ошибки в отдельных полях, не проверяем уникальность
        if not number or not date:
            return cleaned_data
        
        # Проверяем уникальность пары номер+дата
        if self.instance.pk:
            # Редактирование: исключаем текущий объект
            exists = Contract.objects.filter(
                number=number,
                date=date
            ).exclude(pk=self.instance.pk).exists()
        else:
            # Создание: проверяем все записи
            exists = Contract.objects.filter(
                number=number,
                date=date
            ).exists()
        
        if exists:
            raise forms.ValidationError(
                'Договор с таким номером и датой уже существует.'
            )
        
        return cleaned_data


class ResponsiblePersonForm(forms.ModelForm):
    """
    Форма для создания/редактирования ответственного лица.
    Наследуется от ModelForm для автоматического создания полей.
    """
    
    class Meta:
        model = ResponsiblePerson
        fields = ['last_name', 'first_name', 'middle_name', 'position']
        widgets = {
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите фамилию'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя'
            }),
            'middle_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите отчество (при наличии)'
            }),
            'position': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите должность'
            }),
        }
        labels = {
            'last_name': 'Фамилия',
            'first_name': 'Имя',
            'middle_name': 'Отчество',
            'position': 'Должность',
        }
    
    def clean(self):
        """
        Валидация уникальности ФИО (комбинация фамилия+имя+отчество).
        """
        cleaned_data = super().clean()
        last_name = cleaned_data.get('last_name')
        first_name = cleaned_data.get('first_name')
        middle_name = cleaned_data.get('middle_name', '')
        
        # Если есть ошибки в отдельных полях, не проверяем уникальность
        if not last_name or not first_name:
            return cleaned_data
        
        # Проверяем уникальность комбинации ФИО
        if self.instance.pk:
            # Редактирование: исключаем текущий объект
            exists = ResponsiblePerson.objects.filter(
                last_name__iexact=last_name,
                first_name__iexact=first_name,
                middle_name__iexact=middle_name
            ).exclude(pk=self.instance.pk).exists()
        else:
            # Создание: проверяем все записи
            exists = ResponsiblePerson.objects.filter(
                last_name__iexact=last_name,
                first_name__iexact=first_name,
                middle_name__iexact=middle_name
            ).exists()
        
        if exists:
            raise forms.ValidationError(
                'Ответственное лицо с таким ФИО уже существует.'
            )
        
        return cleaned_data
    

class PowerOfAttorneyForm(forms.ModelForm):
    """
    Форма для создания/редактирования доверенности.
    Наследуется от ModelForm для автоматического создания полей.
    
    ВАЖНО: ResponsiblePerson выбирается через модальное окно (HTMX),
    а не через стандартный Select.
    """
    
    # Поле для отображения ФИО ответственного лица (readonly)
    responsible_person_display = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'readonly': 'readonly',
            'placeholder': 'Нажмите "Выбрать" для поиска ответственного лица'
        }),
        label="Ответственное лицо"
    )
    
    class Meta:
        model = PowerOfAttorney
        fields = ['number', 'date', 'responsible_person']  # responsible_person - скрытое поле
        widgets = {
            'number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите номер доверенности (например: 123)'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'  # HTML5 date picker
            }),
            # СКРЫТОЕ ПОЛЕ для ID ответственного лица
            'responsible_person': forms.HiddenInput(attrs={
                'id': 'responsible-person-id'  # Важно для JavaScript
            }),
        }
        labels = {
            'number': 'Номер доверенности',
            'date': 'Дата доверенности',
            'responsible_person': 'Ответственное лицо',
        }
    
    def __init__(self, *args, **kwargs):
        """
        Инициализация формы.
        Заполняем responsible_person_display текущим значением при редактировании.
        """
        super().__init__(*args, **kwargs)
        
        # Если редактируем существующий объект, заполняем отображаемое поле
        if self.instance.pk and self.instance.responsible_person:
            self.fields['responsible_person_display'].initial = str(self.instance.responsible_person)
    
    def clean(self):
        """
        Кросс-полевая валидация уникальности пары номер+дата.
        """
        cleaned_data = super().clean()
        number = cleaned_data.get('number')
        date = cleaned_data.get('date')
        
        # Если есть ошибки в отдельных полях, не проверяем уникальность
        if not number or not date:
            return cleaned_data
        
        # Проверяем уникальность пары номер+дата
        if self.instance.pk:
            # Редактирование: исключаем текущий объект
            exists = PowerOfAttorney.objects.filter(
                number=number,
                date=date
            ).exclude(pk=self.instance.pk).exists()
        else:
            # Создание: проверяем все записи
            exists = PowerOfAttorney.objects.filter(
                number=number,
                date=date
            ).exists()
        
        if exists:
            raise forms.ValidationError(
                'Доверенность с таким номером и датой уже существует.'
            )
        
        return cleaned_data
    


