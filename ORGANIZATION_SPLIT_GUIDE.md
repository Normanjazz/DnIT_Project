# 📘 Разделение ГК/ЧОУ: Полное руководство для новичка

> **Версия:** 1.0  
> **Дата:** 17 марта 2026  
> **Проект:** ДНиТ. Управление. Астрахань  
> **Уровень:** Для начинающих разработчиков Django

---

## 📖 Оглавление

1. [Введение](#введение)
2. [Что такое ГК и ЧОУ?](#что-такое-гк-и-чоу)
3. [Проблема текущей реализации](#проблема-текущей-реализации)
4. [Архитектура решения](#архитектура-решения)
5. [Уровень 1: Модели данных](#уровень-1-модели-данных)
6. [Уровень 2: Формы Django](#уровень-2-формы-django)
7. [Уровень 3: Шаблоны HTML](#уровень-3-шаблоны-html)
8. [Уровень 4: Представления (Views)](#уровень-4-представления-views)
9. [Уровень 5: Миграции](#уровень-5-миграции)
10. [Полный цикл работы](#полный-цикл-работы)
11. [Частые ошибки и как их избежать](#частые-ошибки-и-как-их-избежать)
12. [Контрольный список](#контрольный-список)
13. [Приложение: Справочник терминов](#приложение-справочник-терминов)

---

## 🎯 Введение

Это руководство создано специально для **начинающих разработчиков**, которые только начинают изучать Django и хотят понять, как реализовать разделение данных между двумя организациями в одном приложении.

### Что вы узнаете:

- ✅ Как добавить новое поле в модель Django
- ✅ Как изменить уникальность записей в базе данных
- ✅ Как создать форму с обязательным выбором значения
- ✅ Как отобразить поле в HTML-шаблоне
- ✅ Как фильтровать данные по выбранному значению
- ✅ Как создавать и применять миграции

### Что нужно знать заранее:

- ✅ Основы Python (переменные, функции, классы)
- ✅ Базовое понимание Django (что такое модель, форма, view)
- ✅ Основы HTML (теги, формы, input)

> 💡 **Совет:** Если вы не знакомы с каким-либо термином, загляните в [Приложение: Справочник терминов](#приложение-справочник-терминов) в конце этого руководства.

---

## 🏢 Что такое ГК и ЧОУ?

В контексте этого приложения:

| Аббревиатура | Расшифровка | Описание |
|--------------|-------------|----------|
| **ГК** | Группа компаний | Коммерческая организация, предоставляющая услуги |
| **ЧОУ** | Частное образовательное учреждение | Образовательная организация, предоставляющая услуги |

### Почему нужно разделение?

Обе организации могут работать с **одними и теми же контрагентами**, заключать **договоры с одинаковыми номерами** и выдавать **доверенности с одинаковыми номерами**.

**Пример из жизни:**

```
┌─────────────────────────────────────────────────────────┐
│                    ОДИН КОНТРАГЕНТ                      │
│                 ООО "Управляющая компания"              │
│                     ИНН: 1234567890                     │
└─────────────────────────────────────────────────────────┘
                          │
                          │ Работает с обеими организациями
                          ▼
        ┌─────────────────┴─────────────────┐
        ▼                                   ▼
┌───────────────────┐             ┌───────────────────┐
│       ГК          │             │      ЧОУ          │
│                   │             │                   │
│ Договор №А/1      │             │ Договор №А/1      │
│ от 12.01.2026     │             │ от 12.01.2026     │
│                   │             │                   │
│ Доверенность №100 │             │ Доверенность №100 │
│ от 15.01.2026     │             │ от 15.01.2026     │
└───────────────────┘             └───────────────────┘
```

**Без разделения** база данных будет считать эти договоры **одной и той же записью** и не позволит создать оба договора одновременно!

---

## 🔴 Проблема текущей реализации

### Как сейчас выглядит модель `Contract`:

```python
class Contract(BaseModel):
    number = models.CharField(max_length=50, verbose_name="Номер договора")
    date = models.DateField(verbose_name="Дата договора")
    counterparty = models.ForeignKey(Counterparty, on_delete=models.PROTECT)
    
    class Meta:
        unique_together = ['number', 'date']  # ❌ ПРОБЛЕМА ЗДЕСЬ
```

### Что означает `unique_together = ['number', 'date']`?

Это ограничение базы данных, которое гарантирует:

> **Комбинация номера и даты договора должна быть уникальной.**

### Визуализация проблемы:

```
┌─────────────────────────────────────────────────────────┐
│                    БАЗА ДАННЫХ (сейчас)                 │
└─────────────────────────────────────────────────────────┘

Попытка 1: Создать договор для ГК
┌──────────────────────────────────────────────────────────┐
│ number: "А/1"                                            │
│ date: "2026-01-12"                                       │
│ counterparty: ООО "УК"                                   │
└──────────────────────────────────────────────────────────┘
                    ↓
         ✅ УСПЕХ! Запись создана.
                    ↓
┌────┬──────────┬────────────┬──────────────────┐
│ id │ number   │ date       │ counterparty     │
├────┼──────────┼────────────┼──────────────────┤
│ 1  │ "А/1"    │ 2026-01-12 │ ООО "УК"         │
└────┴──────────┴────────────┴──────────────────┘


Попытка 2: Создать договор для ЧОУ с теми же номером и датой
┌──────────────────────────────────────────────────────────┐
│ number: "А/1"                                            │
│ date: "2026-01-12"                                       │
│ counterparty: ООО "УК"                                   │
└──────────────────────────────────────────────────────────┘
                    ↓
         ❌ ОШИБКА! Нарушение уникальности.
                    ↓
django.db.utils.IntegrityError: 
UNIQUE constraint failed: directories_contract.number, 
directories_contract.date
```

### Почему это происходит?

База данных проверяет уникальность **только по полям `number` и `date`**. Она **не знает** о том, что договоры принадлежат разным организациям.

---

## 🏗️ Архитектура решения

### Общая схема решения:

```
┌─────────────────────────────────────────────────────────────────┐
│                    5 УРОВНЕЙ ИЗМЕНЕНИЙ                          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────┐
│ Уровень 1       │  Модели данных (models.py)
│ ─────────────── │  • Добавить поле organization_type
│ БАЗА ДАННЫХ     │  • Изменить unique_together
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Уровень 2       │  Формы Django (forms.py)
│ ─────────────── │  • Добавить поле в форму
│ ФОРМЫ           │  • Добавить валидацию
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Уровень 3       │  HTML шаблоны (templates/)
│ ─────────────── │  • Отобразить поле выбора
│ ШАБЛОНЫ         │  • Добавить кнопки фильтра
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Уровень 4       │  Представления (views.py)
│ ─────────────── │  • Добавить фильтрацию
│ ЛОГИКА          │  • Обработать выбор
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Уровень 5       │  Миграции (migrations/)
│ ─────────────── │  • Создать миграцию
│ МИГРАЦИИ        │  • Применить к БД
└─────────────────┘
```

### Поток данных при создании договора:

```
┌─────────────────────────────────────────────────────────────────┐
│                    ПОТОК ДАННЫХ                                 │
└─────────────────────────────────────────────────────────────────┘

1. Пользователь
         │
         │ 1. Открывает страницу "Создать договор"
         ▼
2. View (contract_create)
         │
         │ 2. Создаёт пустую форму
         ▼
3. Form (ContractForm)
         │
         │ 3. Генерирует HTML для поля organization_type
         ▼
4. Template (contract_form.html)
         │
         │ 4. Отображает форму в браузере
         ▼
5. Пользователь заполняет форму и нажимает "Сохранить"
         │
         │ 5. POST-запрос с данными
         ▼
6. Form (ContractForm(request.POST))
         │
         │ 6. form.is_valid() → валидация
         │    • Проверка на пустоту
         │    • Проверка уникальности в БД
         ▼
7. View (contract_create)
         │
         │ 7. form.save() → сохранение в БД
         ▼
8. Database (PostgreSQL)
         │
         │ 8. INSERT INTO contract (...)
         ▼
9. Пользователь видит сообщение об успехе
```

---

## 📊 Уровень 1: Модели данных

### Что такое модель Django?

**Модель** — это Python-класс, который описывает, как должна выглядеть таблица в базе данных.

```python
# Пример простой модели
class Contract(models.Model):
    number = models.CharField(max_length=50)  # ← Поле VARCHAR(50) в БД
    date = models.DateField()                 # ← Поле DATE в БД
```

Django **автоматически** превращает этот класс в SQL-запрос:

```sql
CREATE TABLE directories_contract (
    id SERIAL PRIMARY KEY,
    number VARCHAR(50),
    date DATE
);
```

### Шаг 1: Добавляем выбор организаций

```python
# apps/directories/models.py

class Contract(BaseModel):
    # 🔴 ШАГ 1: Определяем варианты выбора
    ORGANIZATION_TYPE_CHOICES = [
        ('GC', 'ГК (Группа компаний)'),
        ('CHOU', 'ЧОУ (Частное образовательное учреждение)'),
    ]
    
    # 🔴 ШАГ 2: Добавляем поле с выбором
    organization_type = models.CharField(
        max_length=10,              # Максимальная длина строки
        choices=ORGANIZATION_TYPE_CHOICES,  # Список вариантов
        verbose_name="Тип организации"
    )
    # ⚠️ Обратите внимание: НЕТ параметра default=
    # Это значит, что поле должно быть заполнено обязательно!
```

### Разбор параметров поля:

| Параметр | Значение | Описание |
|----------|----------|----------|
| `max_length=10` | 10 символов | Максимальная длина строки в БД |
| `choices=...` | `ORGANIZATION_TYPE_CHOICES` | Список допустимых значений |
| `verbose_name=...` | `"Тип организации"` | Человекочитаемое название поля |

### Что такое `choices`?

`choices` — это список кортежей, где:
- **Первый элемент** — значение для хранения в БД (например, `'GC'`)
- **Второй элемент** — отображаемое название (например, `'ГК (Группа компаний)'`)

```python
ORGANIZATION_TYPE_CHOICES = [
    ('GC', 'ГК (Группа компаний)'),      # ← В БД: 'GC', В форме: 'ГК (Группа компаний)'
    ('CHOU', 'ЧОУ (Частное образовательное учреждение)'),
]
```

### Шаг 3: Изменяем уникальность

```python
class Contract(BaseModel):
    # ... поля модели ...
    
    class Meta:
        # ❌ БЫЛО (уникальность по 2 полям):
        # unique_together = ['number', 'date']
        
        # ✅ СТАЛО (уникальность по 3 полям):
        unique_together = ['organization_type', 'number', 'date']
        
        verbose_name = "Договор"
        verbose_name_plural = "Договоры"
        ordering = ['-date', 'number']
```

### Что изменилось?

```
┌─────────────────────────────────────────────────────────┐
│           СРАВНЕНИЕ УНИКАЛЬНОСТИ                        │
└─────────────────────────────────────────────────────────┘

БЫЛО:
┌──────────────────────────────────────────────────────────┐
│ unique_together = ['number', 'date']                     │
│                                                          │
│ Проверка: number='А/1' + date='2026-01-12'              │
│ Результат: ❌ Нельзя создать 2 договора с одинаковыми    │
│            номером и датой (даже для разных организаций) │
└──────────────────────────────────────────────────────────┘

СТАЛО:
┌──────────────────────────────────────────────────────────┐
│ unique_together = ['organization_type', 'number', 'date']│
│                                                          │
│ Проверка: org='GC' + number='А/1' + date='2026-01-12'   │
│ Результат: ✅ Можно создать 2 договора:                  │
│            • ГК: 'А/1' от 12.01.2026                     │
│            • ЧОУ: 'А/1' от 12.01.2026                    │
└──────────────────────────────────────────────────────────┘
```

### Визуализация в базе данных:

```
┌─────────────────────────────────────────────────────────────────┐
│                    БАЗА ДАННЫХ (после изменений)                │
└─────────────────────────────────────────────────────────────────┘

Таблица: directories_contract

┌────┬─────────────────┬──────────┬────────────┬──────────────────┐
│ id │ organization_   │ number   │ date       │ counterparty     │
│    │ type            │          │            │                  │
├────┼─────────────────┼──────────┼────────────┼──────────────────┤
│ 1  │ 'GC'            │ 'А/1'    │ 2026-01-12 │ ООО "УК"         │
│ 2  │ 'CHOU'          │ 'А/1'    │ 2026-01-12 │ ООО "УК"         │ ← ✅ МОЖНО!
│ 3  │ 'GC'            │ 'А/2'    │ 2026-01-15 │ АО "Вектор"      │
│ 4  │ 'CHOU'          │ '15-У'   │ 2026-01-20 │ ИП Иванов        │
└────┴─────────────────┴──────────┴────────────┴──────────────────┘

Попытка создать дубликат:
┌────┬─────────────────┬──────────┬────────────┬──────────────────┐
│ 5  │ 'GC'            │ 'А/1'    │ 2026-01-12 │ ИП Петров        │ ← ❌ НЕЛЬЗЯ!
└────┴─────────────────┴──────────┴────────────┴──────────────────┘
         ↑                      ↑           ↑
         └──────────────────────┴───────────┘
              Эта комбинация уже есть (id=1)
```

### Полный код модели Contract:

```python
# apps/directories/models.py

from django.db import models
from apps.core.models import BaseModel
from .models import Counterparty


class Contract(BaseModel):
    """
    Справочник договоров. Связан с контрагентом (один ко многим).
    """
    
    # 🔴 ВЫБОР ОРГАНИЗАЦИИ
    ORGANIZATION_TYPE_CHOICES = [
        ('GC', 'ГК (Группа компаний)'),
        ('CHOU', 'ЧОУ (Частное образовательное учреждение)'),
    ]
    
    # 🔴 ПОЛЕ ТИПА ОРГАНИЗАЦИИ
    organization_type = models.CharField(
        max_length=10,
        choices=ORGANIZATION_TYPE_CHOICES,
        verbose_name="Тип организации"
    )
    
    # Основные поля
    number = models.CharField(
        max_length=50,
        verbose_name="Номер договора"
    )
    
    date = models.DateField(
        verbose_name="Дата договора"
    )
    
    # Связь с контрагентом
    counterparty = models.ForeignKey(
        Counterparty,
        on_delete=models.PROTECT,
        related_name='contracts',
        verbose_name="Контрагент"
    )
    
    class Meta:
        verbose_name = "Договор"
        verbose_name_plural = "Договоры"
        ordering = ['-date', 'number']
        
        # ✅ УНИКАЛЬНОСТЬ ПО 3 ПОЛЯМ
        unique_together = ['organization_type', 'number', 'date']
        
        indexes = [
            models.Index(fields=['organization_type']),
            models.Index(fields=['number']),
            models.Index(fields=['date']),
        ]
    
    def __str__(self):
        return f"{self.number} от {self.date.strftime('%d.%m.%Y')}"
```

### Применяем к другим моделям:

Аналогичные изменения нужно сделать в моделях `PowerOfAttorney` и `WorkType`:

```python
# apps/directories/models.py

class PowerOfAttorney(BaseModel):
    """
    Справочник доверенностей.
    """
    
    ORGANIZATION_TYPE_CHOICES = [
        ('GC', 'ГК (Группа компаний)'),
        ('CHOU', 'ЧОУ (Частное образовательное учреждение)'),
    ]
    
    organization_type = models.CharField(
        max_length=10,
        choices=ORGANIZATION_TYPE_CHOICES,
        verbose_name="Тип организации"
    )
    
    number = models.CharField(
        max_length=50,
        verbose_name="Номер доверенности"
    )
    
    date = models.DateField(
        verbose_name="Дата доверенности"
    )
    
    responsible_person = models.ForeignKey(
        ResponsiblePerson,
        on_delete=models.PROTECT,
        related_name='powers_of_attorney',
        verbose_name="Ответственное лицо"
    )
    
    class Meta:
        verbose_name = "Доверенность"
        verbose_name_plural = "Доверенности"
        ordering = ['-date', 'number']
        
        # ✅ УНИКАЛЬНОСТЬ ПО 3 ПОЛЯМ
        unique_together = ['organization_type', 'number', 'date']
        
        indexes = [
            models.Index(fields=['organization_type']),
            models.Index(fields=['number']),
            models.Index(fields=['date']),
        ]
    
    def __str__(self):
        return f"№{self.number} от {self.date.strftime('%d.%m.%Y')}"


class WorkType(BaseModel):
    """
    Справочник видов работ.
    """
    
    ORGANIZATION_TYPE_CHOICES = [
        ('GC', 'ГК (Группа компаний)'),
        ('CHOU', 'ЧОУ (Частное образовательное учреждение)'),
    ]
    
    organization_type = models.CharField(
        max_length=10,
        choices=ORGANIZATION_TYPE_CHOICES,
        verbose_name="Тип организации"
    )
    
    full_name = models.CharField(
        max_length=500,
        verbose_name="Полное наименование"
    )
    
    short_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Сокращённое наименование"
    )
    
    class Meta:
        verbose_name = "Вид работ"
        verbose_name_plural = "Виды работ"
        
        # ✅ СОРТИРОВКА ПО ОРГАНИЗАЦИИ
        ordering = ['organization_type', 'full_name']
        
        indexes = [
            models.Index(fields=['organization_type']),
            models.Index(fields=['full_name']),
        ]
    
    def __str__(self):
        return self.full_name
```

---

## 📝 Уровень 2: Формы Django

### Что такое Django Form?

**Форма Django** — это класс, который:
1. Генерирует HTML-код для полей ввода
2. Проверяет (валидирует) данные, отправленные пользователем
3. Сохраняет данные в модель

### Типы форм:

| Тип | Описание | Когда использовать |
|-----|----------|-------------------|
| `forms.Form` | Обычная форма | Для произвольных данных (например, форма поиска) |
| `forms.ModelForm` | Форма на основе модели | Для CRUD-операций с моделью |

Мы используем **`ModelForm`**, потому что работаем с моделями.

### Шаг 1: Добавляем поле вручную

Почему вручную? Потому что нам нужно:
- ❌ **Без значения по умолчанию** (чтобы пользователь не забыл выбрать)
- ✅ **С обязательной валидацией** (чтобы нельзя было сохранить пустым)

```python
# apps/directories/forms.py

from django import forms
from .models import Contract


class ContractForm(forms.ModelForm):
    """
    Форма для создания/редактирования договора.
    """
    
    # 🔴 ДОБАВЛЯЕМ ПОЛЕ ВРУЧНУЮ
    organization_type = forms.ChoiceField(
        choices=Contract.ORGANIZATION_TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'  # Bootstrap класс для красивого select
        }),
        label="Тип организации",
        required=True  # Обязательно для заполнения
    )
    
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
        # ✅ ВКЛЮЧАЕМ organization_type В ПОЛЯ ФОРМЫ
        fields = ['organization_type', 'number', 'date', 'counterparty']
        widgets = {
            'number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите номер договора (например: 12-А)'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'  # HTML5 date picker
            }),
            'counterparty': forms.HiddenInput(attrs={
                'id': 'counterparty-id'
            }),
        }
        labels = {
            'number': 'Номер договора',
            'date': 'Дата договора',
            'counterparty': 'Контрагент',
        }
```

### Разбор `ChoiceField`:

```python
organization_type = forms.ChoiceField(
    choices=Contract.ORGANIZATION_TYPE_CHOICES,  # Список вариантов
    widget=forms.Select(attrs={                  # HTML виджет (выпадающий список)
        'class': 'form-select'                   # Bootstrap класс
    }),
    label="Тип организации",                     # Подпись к полю
    required=True                                # Обязательно для заполнения
)
```

### Что такое `widget`?

**Widget** — это класс, который определяет, как поле формы будет выглядеть в HTML.

```python
# Разные виджеты для разных полей:

forms.TextInput()      # → <input type="text">
forms.DateInput()      # → <input type="date">
forms.Select()         # → <select><option>...</option></select>
forms.HiddenInput()    # → <input type="hidden">
forms.Textarea()       # → <textarea></textarea>
```

### Шаг 2: Инициализация формы

Метод `__init__` вызывается при создании формы. Нам нужно:
- Установить текущее значение при редактировании
- Заполнить отображаемое поле контрагента

```python
class ContractForm(forms.ModelForm):
    # ... поля формы ...
    
    def __init__(self, *args, **kwargs):
        """
        Инициализация формы.
        Вызывается при создании формы: ContractForm() или ContractForm(request.POST)
        """
        super().__init__(*args, **kwargs)  # Вызываем конструктор родительского класса
        
        # 🔴 ЕСЛИ РЕДАКТИРУЕМ существующий объект
        if self.instance.pk and self.instance.organization_type:
            # Устанавливаем начальное значение поля
            self.fields['organization_type'].initial = self.instance.organization_type
        
        # Заполняем counterparty_display текущим значением
        if self.instance.pk and self.instance.counterparty:
            self.fields['counterparty_display'].initial = self.instance.counterparty.name
```

### Разбор `__init__`:

```python
# Что такое self.instance?

# При создании новой записи:
form = ContractForm()
# self.instance → новый пустой объект Contract()
# self.instance.pk → None (объект ещё не сохранён в БД)

# При редактировании существующей записи:
form = ContractForm(instance=contract)
# self.instance → существующий объект Contract
# self.instance.pk → id объекта (например, 5)
# self.instance.organization_type → 'GC'
```

### Шаг 3: Валидация уникальности

Метод `clean()` используется для **кросс-полевой валидации** — проверки нескольких полей одновременно.

```python
class ContractForm(forms.ModelForm):
    # ... поля формы ...
    
    def clean(self):
        """
        Кросс-полевая валидация уникальности.
        Проверяет, что договор с таким номером и датой 
        не существует для выбранной организации.
        """
        # 🔴 ПОЛУЧАЕМ ОЧИЩЕННЫЕ ДАННЫЕ
        cleaned_data = super().clean()
        
        organization_type = cleaned_data.get('organization_type')
        number = cleaned_data.get('number')
        date = cleaned_data.get('date')
        
        # 🔴 ЕСЛИ ЕСТЬ ОШИБКИ В ОТДЕЛЬНЫХ ПОЛЯХ, не проверяем уникальность
        if not organization_type or not number or not date:
            return cleaned_data
        
        # 🔴 ПРОВЕРЯЕМ УНИКАЛЬНОСТЬ С УЧЁТОМ ОРГАНИЗАЦИИ
        if self.instance.pk:
            # РЕДАКТИРОВАНИЕ: исключаем текущий объект из проверки
            exists = Contract.objects.filter(
                organization_type=organization_type,
                number=number,
                date=date
            ).exclude(pk=self.instance.pk).exists()
        else:
            # СОЗДАНИЕ: проверяем все записи
            exists = Contract.objects.filter(
                organization_type=organization_type,
                number=number,
                date=date
            ).exists()
        
        # 🔴 ЕСЛИ НАЙДЕН ДУБЛИКАТ, добавляем ошибку
        if exists:
            # Получаем человеческое название организации
            org_display = dict(Contract.ORGANIZATION_TYPE_CHOICES)[organization_type]
            
            raise forms.ValidationError(
                f'Договор с номером "{number}" от {date.strftime("%d.%m.%Y")} '
                f'уже существует для {org_display}.'
            )
        
        return cleaned_data
```

### Как работает `clean()`?

```
┌─────────────────────────────────────────────────────────────────┐
│                    ПОТОК МЕТОДА clean()                         │
└─────────────────────────────────────────────────────────────────┘

1. cleaned_data = super().clean()
         │
         │ Вызываем родительский clean() для получения данных
         │ После этого cleaned_data содержит:
         │ {
         │     'organization_type': 'GC',
         │     'number': 'А/1',
         │     'date': datetime.date(2026, 1, 12),
         │     'counterparty': 5
         │ }
         ▼
2. if not organization_type or not number or not date:
         │
         │ Если хотя бы одно поле пустое, пропускаем проверку
         │ (ошибки уже добавлены в других clean_<field>() методах)
         ▼
3. if self.instance.pk:
         │
         │ Проверяем, редактируем ли мы существующий объект
         │
         ├─ ДА (редактирование):
         │    exists = Contract.objects.filter(...).exclude(pk=self.instance.pk)
         │    ↑ Исключаем текущий объект из проверки
         │
         └─ НЕТ (создание):
              exists = Contract.objects.filter(...)
              ↑ Проверяем все записи
         ▼
4. if exists:
         │
         │ Если дубликат найден, выбрасываем ошибку
         │
         ▼
5. raise forms.ValidationError(...)
         │
         │ Ошибка добавляется в form.errors
         │ Форма возвращается пользователю с сообщением об ошибке
```

### Что такое `cleaned_data`?

```python
# Пример:

# ДО вызова clean():
# request.POST содержит "сырые" данные:
{
    'organization_type': 'GC',
    'number': 'А/1',
    'date': '2026-01-12',  # ← Строка!
    'counterparty': '5'    # ← Строка!
}

# ПОСЛЕ вызова clean():
# cleaned_data содержит обработанные данные:
{
    'organization_type': 'GC',
    'number': 'А/1',
    'date': datetime.date(2026, 1, 12),  # ← date объект!
    'counterparty': 5                     # ← int!
}
```

### Полный код формы ContractForm:

```python
# apps/directories/forms.py

from django import forms
from django.core.exceptions import ValidationError
from .models import WorkType, Unit, Counterparty, Contract, ResponsiblePerson, PowerOfAttorney


class ContractForm(forms.ModelForm):
    """
    Форма для создания/редактирования договора.
    """
    
    # 🔴 ПОЛЕ ТИПА ОРГАНИЗАЦИИ (вручную, без default)
    organization_type = forms.ChoiceField(
        choices=Contract.ORGANIZATION_TYPE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label="Тип организации",
        required=True
    )
    
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
        fields = ['organization_type', 'number', 'date', 'counterparty']
        widgets = {
            'number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите номер договора (например: 12-А)'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'counterparty': forms.HiddenInput(attrs={
                'id': 'counterparty-id'
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
        """
        super().__init__(*args, **kwargs)
        
        # Если редактируем существующий объект, устанавливаем текущее значение
        if self.instance.pk and self.instance.organization_type:
            self.fields['organization_type'].initial = self.instance.organization_type
        
        # Если редактируем, заполняем counterparty_display
        if self.instance.pk and self.instance.counterparty:
            self.fields['counterparty_display'].initial = self.instance.counterparty.name
    
    def clean(self):
        """
        Кросс-полевая валидация уникальности пары номер+дата + организация.
        """
        cleaned_data = super().clean()
        
        organization_type = cleaned_data.get('organization_type')
        number = cleaned_data.get('number')
        date = cleaned_data.get('date')
        
        # Если есть ошибки в отдельных полях, не проверяем уникальность
        if not organization_type or not number or not date:
            return cleaned_data
        
        # Проверка уникальности с учётом организации
        if self.instance.pk:
            # Редактирование: исключаем текущий объект
            exists = Contract.objects.filter(
                organization_type=organization_type,
                number=number,
                date=date
            ).exclude(pk=self.instance.pk).exists()
        else:
            # Создание: проверяем все записи
            exists = Contract.objects.filter(
                organization_type=organization_type,
                number=number,
                date=date
            ).exists()
        
        if exists:
            # Получаем человеческое название организации
            org_display = dict(Contract.ORGANIZATION_TYPE_CHOICES)[organization_type]
            raise forms.ValidationError(
                f'Договор с номером "{number}" от {date.strftime("%d.%m.%Y")} '
                f'уже существует для {org_display}.'
            )
        
        return cleaned_data
```

### Применяем к другим формам:

Аналогичные изменения нужно сделать в формах `PowerOfAttorneyForm` и `WorkTypeForm`:

```python
# apps/directories/forms.py

class PowerOfAttorneyForm(forms.ModelForm):
    """
    Форма для создания/редактирования доверенности.
    """
    
    organization_type = forms.ChoiceField(
        choices=PowerOfAttorney.ORGANIZATION_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Тип организации",
        required=True
    )
    
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
        fields = ['organization_type', 'number', 'date', 'responsible_person']
        widgets = {
            'number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите номер доверенности (например: 123)'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'responsible_person': forms.HiddenInput(attrs={
                'id': 'responsible-person-id'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance.pk and self.instance.organization_type:
            self.fields['organization_type'].initial = self.instance.organization_type
        
        if self.instance.pk and self.instance.responsible_person:
            self.fields['responsible_person_display'].initial = str(self.instance.responsible_person)
    
    def clean(self):
        cleaned_data = super().clean()
        
        organization_type = cleaned_data.get('organization_type')
        number = cleaned_data.get('number')
        date = cleaned_data.get('date')
        
        if not organization_type or not number or not date:
            return cleaned_data
        
        if self.instance.pk:
            exists = PowerOfAttorney.objects.filter(
                organization_type=organization_type,
                number=number,
                date=date
            ).exclude(pk=self.instance.pk).exists()
        else:
            exists = PowerOfAttorney.objects.filter(
                organization_type=organization_type,
                number=number,
                date=date
            ).exists()
        
        if exists:
            org_display = dict(PowerOfAttorney.ORGANIZATION_TYPE_CHOICES)[organization_type]
            raise forms.ValidationError(
                f'Доверенность с номером "{number}" от {date.strftime("%d.%m.%Y")} '
                f'уже существует для {org_display}.'
            )
        
        return cleaned_data


class WorkTypeForm(forms.ModelForm):
    """
    Форма для создания/редактирования вида работ.
    """
    
    organization_type = forms.ChoiceField(
        choices=WorkType.ORGANIZATION_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Тип организации",
        required=True
    )
    
    class Meta:
        model = WorkType
        fields = ['organization_type', 'full_name', 'short_name']
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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance.pk and self.instance.organization_type:
            self.fields['organization_type'].initial = self.instance.organization_type
    
    def clean_full_name(self):
        """
        Валидация уникальности полного наименования с учётом организации.
        """
        full_name = self.cleaned_data.get('full_name')
        organization_type = self.cleaned_data.get('organization_type')
        
        if not full_name or not organization_type:
            return full_name
        
        if self.instance.pk:
            exists = WorkType.objects.filter(
                full_name__iexact=full_name,
                organization_type=organization_type
            ).exclude(pk=self.instance.pk).exists()
        else:
            exists = WorkType.objects.filter(
                full_name__iexact=full_name,
                organization_type=organization_type
            ).exists()
        
        if exists:
            org_display = dict(WorkType.ORGANIZATION_TYPE_CHOICES)[organization_type]
            raise forms.ValidationError(
                f'Вид работ с таким наименованием уже существует для {org_display}.'
            )
        
        return full_name
```

---

## 🎨 Уровень 3: Шаблоны HTML

### Что такое Django Template?

**Шаблон Django** — это HTML-файл со специальными тегами, которые позволяют:
- Вставлять данные из Python (`{{ variable }}`)
- Использовать логику (`{% if %}`, `{% for %}`)
- Наследовать структуру (`{% extends %}`)

### Шаг 1: Отображение поля в форме

```html+django
{# templates/directories/contract_form.html #}

{% extends 'base.html' %}

{% block title %}{{ page_title }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-12">
            <h1>{{ page_title }}</h1>
            
            <form method="post" novalidate>
                {% csrf_token %}
                
                {# 🔴 ПОЛЕ ТИПА ОРГАНИЗАЦИИ - ПЕРВОЕ ПОЛЕ #}
                <div class="mb-3">
                    <label for="{{ form.organization_type.id_for_label }}" class="form-label">
                        {{ form.organization_type.label }}
                        <span class="text-danger">*</span>
                    </label>
                    {{ form.organization_type }}
                    {% if form.organization_type.errors %}
                        <div class="invalid-feedback d-block">
                            {{ form.organization_type.errors.0 }}
                        </div>
                    {% endif %}
                    <div class="form-text">
                        Выберите организацию, для которой создаётся договор
                    </div>
                </div>
                
                {# Поле номера договора #}
                <div class="mb-3">
                    <label for="{{ form.number.id_for_label }}" class="form-label">
                        {{ form.number.label }}
                    </label>
                    {{ form.number }}
                    {% if form.number.errors %}
                        <div class="invalid-feedback d-block">
                            {{ form.number.errors.0 }}
                        </div>
                    {% endif %}
                </div>
                
                {# Поле даты договора #}
                <div class="mb-3">
                    <label for="{{ form.date.id_for_label }}" class="form-label">
                        {{ form.date.label }}
                    </label>
                    {{ form.date }}
                    {% if form.date.errors %}
                        <div class="invalid-feedback d-block">
                            {{ form.date.errors.0 }}
                        </div>
                    {% endif %}
                </div>
                
                {# Поле контрагента (скрытое) #}
                {{ form.counterparty }}
                
                {# Поле для отображения контрагента #}
                <div class="mb-3">
                    <label for="{{ form.counterparty_display.id_for_label }}" class="form-label">
                        {{ form.counterparty_display.label }}
                    </label>
                    <div class="input-group">
                        {{ form.counterparty_display }}
                        <button type="button" class="btn btn-outline-secondary" data-bs-toggle="modal" data-bs-target="#modalCounterparty">
                            Выбрать
                        </button>
                    </div>
                    {% if form.counterparty_display.errors %}
                        <div class="invalid-feedback d-block">
                            {{ form.counterparty_display.errors.0 }}
                        </div>
                    {% endif %}
                </div>
                
                <div class="d-flex gap-2">
                    <button type="submit" class="btn btn-primary">
                        <i class="bi bi-save"></i> Сохранить
                    </button>
                    <a href="{% url 'directories:contract_list' %}" class="btn btn-secondary">
                        Отмена
                    </a>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}
```

### Разбор синтаксиса:

```django
{# Это комментарий Django #}

{{ form.organization_type }}           {# Вывод значения переменной #}
{{ form.organization_type.label }}     {# Вывод подписи к полю #}
{{ form.organization_type.errors }}    {# Вывод ошибок валидации #}

{% if form.organization_type.errors %}  {# Условие #}
    <div class="invalid-feedback">...</div>
{% endif %}

{% url 'directories:contract_list' %}   {# Генерация URL #}
```

### Как это выглядит в браузере:

```
┌─────────────────────────────────────────────────────────┐
│                    Создать договор                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Тип организации *                                       │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Выберите организацию...                             ▼ │ │
│ └─────────────────────────────────────────────────────┘ │
│ Выберите организацию, для которой создаётся договор     │
│                                                         │
│ Номер договора                                          │
│ ┌─────────────────────────────────────────────────────┐ │
│ │                                                     │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                         │
│ Дата договора                                           │
│ ┌─────────────────────────────────────────────────────┐ │
│ │__.__.____                                            │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                         │
│ Контрагент                                              │
│ ┌─────────────────────────────┐ ┌─────────────────────┐ │
│ │                             │ │     Выбрать         │ │
│ └─────────────────────────────┘ └─────────────────────┘ │
│                                                         │
│ [Сохранить] [Отмена]                                    │
└─────────────────────────────────────────────────────────┘
```

### При клике на select:

```
┌─────────────────────────────────────────────────────────┐
│ Тип организации *                                       │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ ГК (Группа компаний)                                ▼ │ │
│ ├─────────────────────────────────────────────────────┤ │
│ │ ☑ ГК (Группа компаний)                              │ │
│ │   ЧОУ (Частное образовательное учреждение)          │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### Если пользователь забыл выбрать организацию:

```
┌─────────────────────────────────────────────────────────┐
│                    Создать договор                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Тип организации *                                       │
│ ┌─────────────────────────────────────────────────────┐ │
│ │                                                     ▼ │ │
│ └─────────────────────────────────────────────────────┘ │
│ ⚠️ Это поле обязательно.                                │
│                                                         │
│ ... остальные поля ...                                  │
└─────────────────────────────────────────────────────────┘
```

### Если дубликат договора:

```
┌─────────────────────────────────────────────────────────┐
│                    Создать договор                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Тип организации *                                       │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ ГК (Группа компаний)                                ▼ │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                         │
│ Номер договора                                          │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ А/1                                                 │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                         │
│ Дата договора                                           │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ 12.01.2026                                          │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                         │
│ ⚠️ Договор с номером "А/1" от 12.01.2026 уже           │
│    существует для ГК (Группа компаний).                 │
│                                                         │
│ [Сохранить] [Отмена]                                    │
└─────────────────────────────────────────────────────────┘
```

### Шаг 2: Кнопки фильтра в списке

```html+django
{# templates/directories/contract_list.html #}

{% extends 'base.html' %}

{% block title %}{{ page_title }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-12">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h1>{{ page_title }}</h1>
                <a href="{% url 'directories:contract_create' %}" class="btn btn-primary">
                    <i class="bi bi-plus-lg"></i> Создать договор
                </a>
            </div>
            
            {# 🔴 ФИЛЬТР ПО ОРГАНИЗАЦИИ #}
            <div class="btn-group mb-3" role="group">
                <a href="?{% if search_query %}q={{ search_query }}{% endif %}" 
                   class="btn {% if not org_type %}btn-primary{% else %}btn-outline-primary{% endif %}">
                    Все
                </a>
                <a href="?org_type=GC{% if search_query %}&q={{ search_query }}{% endif %}" 
                   class="btn {% if org_type == 'GC' %}btn-primary{% else %}btn-outline-primary{% endif %}">
                    ГК
                </a>
                <a href="?org_type=CHOU{% if search_query %}&q={{ search_query }}{% endif %}" 
                   class="btn {% if org_type == 'CHOU' %}btn-primary{% else %}btn-outline-primary{% endif %}">
                    ЧОУ
                </a>
            </div>
            
            {# Поиск #}
            <form method="get" class="mb-3">
                <div class="input-group">
                    <input type="text" name="q" class="form-control" 
                           placeholder="Поиск по номеру или контрагенту..."
                           value="{{ search_query }}">
                    {% if org_type %}
                        <input type="hidden" name="org_type" value="{{ org_type }}">
                    {% endif %}
                    <button type="submit" class="btn btn-outline-secondary">
                        <i class="bi bi-search"></i> Найти
                    </button>
                </div>
            </form>
            
            {# Таблица договоров #}
            <table class="table table-hover">
                <thead>
                    <tr>
                        <th>Организация</th>
                        <th>Номер</th>
                        <th>Дата</th>
                        <th>Контрагент</th>
                        <th>Действия</th>
                    </tr>
                </thead>
                <tbody>
                    {% for contract in contracts %}
                    <tr>
                        <td>
                            {% if contract.organization_type == 'GC' %}
                                <span class="badge bg-primary">ГК</span>
                            {% else %}
                                <span class="badge bg-success">ЧОУ</span>
                            {% endif %}
                        </td>
                        <td>{{ contract.number }}</td>
                        <td>{{ contract.date|date:"d.m.Y" }}</td>
                        <td>{{ contract.counterparty.name }}</td>
                        <td>
                            <div class="btn-group btn-group-sm">
                                <a href="{% url 'directories:contract_detail' contract.pk %}" 
                                   class="btn btn-info">
                                    <i class="bi bi-eye"></i>
                                </a>
                                <a href="{% url 'directories:contract_update' contract.pk %}" 
                                   class="btn btn-warning">
                                    <i class="bi bi-pencil"></i>
                                </a>
                                <a href="{% url 'directories:contract_delete' contract.pk %}" 
                                   class="btn btn-danger">
                                    <i class="bi bi-trash"></i>
                                </a>
                            </div>
                        </td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="5" class="text-center text-muted">
                            {% if search_query or org_type %}
                                Ничего не найдено. Попробуйте изменить параметры поиска.
                            {% else %}
                                Договоры ещё не созданы. Нажмите "Создать договор", чтобы добавить первый.
                            {% endif %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}
```

### Разбор кнопок фильтра:

```django
{# Кнопка "Все" #}
<a href="?{% if search_query %}q={{ search_query }}{% endif %}" 
   class="btn {% if not org_type %}btn-primary{% else %}btn-outline-primary{% endif %}">
    Все
</a>

{# Что происходит: #}
{# • Если org_type не задан → кнопка синяя (активна) #}
{# • Если org_type задан → кнопка контурная (неактивна) #}
{# • URL: ? (сброс фильтра) или ?q=поиск (сохранение поиска) #}


{# Кнопка "ГК" #}
<a href="?org_type=GC{% if search_query %}&q={{ search_query }}{% endif %}" 
   class="btn {% if org_type == 'GC' %}btn-primary{% else %}btn-outline-primary{% endif %}">
    ГК
</a>

{# Что происходит: #}
{# • URL: ?org_type=GC или ?org_type=GC&q=поиск #}
{# • Если org_type == 'GC' → кнопка синяя (активна) #}


{# Кнопка "ЧОУ" #}
<a href="?org_type=CHOU{% if search_query %}&q={{ search_query }}{% endif %}" 
   class="btn {% if org_type == 'CHOU' %}btn-primary{% else %}btn-outline-primary{% endif %}">
    ЧОУ
</a>
```

### Как это выглядит в браузере:

```
┌─────────────────────────────────────────────────────────┐
│ Договоры                        [+ Создать договор]     │
├─────────────────────────────────────────────────────────┤
│ [Все] [ ГК ] [ ЧОУ ]  ← Активна кнопка "Все"            │
├─────────────────────────────────────────────────────────┤
│ ┌───────────────────────────────────────────────────┐   │
│ │ Поиск по номеру или контрагенту...        [🔍]    │   │
│ └───────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│ Организация │ Номер │ Дата       │ Контрагент │ ...    │
├─────────────┼───────┼────────────┼────────────┼────────┤
│    [ГК]     │ А/1   │ 12.01.2026 │ ООО "Ромашка"│ ...  │
│   [ЧОУ]     │ А/1   │ 12.01.2026 │ ООО "Ромашка"│ ...  │
│    [ГК]     │ 15-Д  │ 15.01.2026 │ АО "Вектор"  │ ...  │
└─────────────────────────────────────────────────────────┘

При клике на "ГК":
┌─────────────────────────────────────────────────────────┐
│ Договоры                                                │
├─────────────────────────────────────────────────────────┤
│ [Все] [ ГК ] [ ЧОУ ]  ← Активна кнопка "ГК"             │
├─────────────────────────────────────────────────────────┤
│ Организация │ Номер │ Дата       │ Контрагент │ ...    │
├─────────────┼───────┼────────────┼────────────┼────────┤
│    [ГК]     │ А/1   │ 12.01.2026 │ ООО "Ромашка"│ ...  │
│    [ГК]     │ 15-Д  │ 15.01.2026 │ АО "Вектор"  │ ...  │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 Уровень 4: Представления (Views)

### Что такое View?

**View (представление)** — это Python-функция, которая:
1. Получает HTTP-запрос от пользователя
2. Обрабатывает данные (из формы, из БД)
3. Возвращает HTTP-ответ (HTML-страницу, редирект, ошибку)

### Шаг 1: Добавляем фильтрацию в список

```python
# apps/directories/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import WorkType, Unit, Counterparty, Contract, ResponsiblePerson, PowerOfAttorney
from .forms import WorkTypeForm, UnitForm, CounterpartyForm, ContractForm, ResponsiblePersonForm, PowerOfAttorneyForm


@login_required
def contract_list(request):
    """
    Список договоров с поиском, фильтрацией по организации.
    """
    # Получаем все неархивированные договоры с связанными контрагентами
    contracts = Contract.objects.select_related('counterparty').all()
    
    # 🔴 ФИЛЬТР ПО ОРГАНИЗАЦИИ
    org_type = request.GET.get('org_type', '')
    if org_type in ['GC', 'CHOU']:
        contracts = contracts.filter(organization_type=org_type)
    
    # Поиск по номеру или наименованию контрагента
    search_query = request.GET.get('q', '')
    if search_query:
        contracts = contracts.filter(
            Q(number__icontains=search_query) |
            Q(counterparty__name__icontains=search_query)
        )
    
    # Сортировка
    contracts = contracts.order_by('-date', 'number')
    
    context = {
        'contracts': contracts,
        'search_query': search_query,
        'org_type': org_type,  # Для подсветки активной кнопки
        'page_title': 'Договоры',
    }
    
    return render(request, 'directories/contract_list.html', context)
```

### Разбор фильтрации:

```python
# 🔴 request.GET.get('org_type', '')

# Что такое request.GET?
# Это словарь с параметрами из URL (всё, что после ?)

# Примеры URL и содержимое request.GET:

# URL: /directories/contracts/
# request.GET = {}
# request.GET.get('org_type', '') → '' (пустая строка, значение по умолчанию)

# URL: /directories/contracts/?org_type=GC
# request.GET = {'org_type': 'GC'}
# request.GET.get('org_type', '') → 'GC'

# URL: /directories/contracts/?org_type=CHOU&q=ромашка
# request.GET = {'org_type': 'CHOU', 'q': 'ромашка'}
# request.GET.get('org_type', '') → 'CHOU'
# request.GET.get('q', '') → 'ромашка'


# 🔴 if org_type in ['GC', 'CHOU']:

# Проверяем, что значение корректное (защита от инъекций)
# Если org_type = '' или что-то другое → фильтрация не применяется


# 🔴 contracts = contracts.filter(organization_type=org_type)

# Применяем фильтр к QuerySet
# Это создаёт новый QuerySet с условием WHERE organization_type = 'GC'

# SQL-эквивалент:
# SELECT * FROM directories_contract
# WHERE organization_type = 'GC' AND is_archived = FALSE
```

### Как работает QuerySet:

```python
# QuerySet — это "ленивый" запрос к БД
# Он не выполняется, пока не будет вызван (например, в шаблоне)

# Цепочка фильтров:

contracts = Contract.objects.all()
# ← QuerySet: SELECT * FROM directories_contract

contracts = contracts.filter(organization_type='GC')
# ← QuerySet: SELECT * FROM directories_contract WHERE organization_type='GC'

contracts = contracts.filter(number__icontains='А')
# ← QuerySet: SELECT * FROM directories_contract WHERE organization_type='GC' AND number LIKE '%А%'

contracts = contracts.order_by('-date')
# ← QuerySet: SELECT * FROM directories_contract WHERE ... ORDER BY date DESC

# Запрос выполняется только здесь:
for contract in contracts:  # ← В шаблоне {% for contract in contracts %}
    print(contract.number)
```

### Шаг 2: Создание договора (без изменений)

View для создания договора **не требует изменений**, потому что вся валидация уже в форме:

```python
@login_required
def contract_create(request):
    """
    Создание нового договора.
    """
    form = ContractForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():  # ← Вся валидация здесь!
            contract = form.save(commit=False)
            contract.created_by = request.user
            contract.save()
            
            messages.success(request, f'Договор "{contract.number}" успешно создан!')
            return redirect('directories:contract_list')
    
    context = {
        'form': form,
        'page_title': 'Создать договор',
        'action': 'create',
    }
    return render(request, 'directories/contract_form.html', context)
```

### Почему view не меняется?

```
┌─────────────────────────────────────────────────────────┐
│                    Django Forms Flow                    │
└─────────────────────────────────────────────────────────┘

1. form = ContractForm(request.POST or None)
         │
         │ Создаёт форму с данными (POST) или пустую (None)
         ▼
2. if request.method == 'POST':
         │
         │ Проверяем, что это POST-запрос (отправка формы)
         ▼
3. if form.is_valid():
         │
         │ Запускает ВСЮ валидацию:
         │ • Встроенную (required, max_length)
         │ • clean_<field>() для каждого поля
         │ • clean() для кросс-полевой валидации
         │
         │ Если есть ошибки → возвращает False
         │ Если всё ок → возвращает True
         ▼
4. contract = form.save()
         │
         │ Сохраняет данные в БД
         ▼
5. redirect('directories:contract_list')
         │
         │ Перенаправляет на список
```

**Вывод:** Вся логика валидации уже в форме. View только вызывает `form.is_valid()`.

---

## 🔄 Уровень 5: Миграции

### Что такое миграции?

**Миграции** — это способ Django синхронизировать код моделей с базой данных.

### Зачем нужны миграции?

```
┌─────────────────────────────────────────────────────────┐
│                    ПРОБЛЕМА                             │
└─────────────────────────────────────────────────────────┘

Вы изменили модель (models.py):
┌──────────────────────────────────────────────────────────┐
│ class Contract(BaseModel):                               │
│     organization_type = models.CharField(...)  ← НОВОЕ!  │
│     unique_together = ['organization_type', 'number', 'date']
└──────────────────────────────────────────────────────────┘

Но база данных об этом НЕ ЗНАЕТ!
┌──────────────────────────────────────────────────────────┐
│ Таблица в БД: directories_contract                       │
│ ┌────┬──────────┬────────────┬──────────────────┐        │
│ │ id │ number   │ date       │ counterparty_id  │        │
│ ├────┼──────────┼────────────┼──────────────────┤        │
│ │ 1  │ "А/1"    │ 2026-01-12 │ 5                │        │
│ └────┴──────────┴────────────┴──────────────────┘        │
│                                                          │
│ ❌ НЕТ ПОЛЯ organization_type!                           │
└──────────────────────────────────────────────────────────┘

Нужно обновить БД → Для этого нужны миграции!
```

### Шаг 1: Создание миграции

```bash
# Перейдите в папку проекта
cd C:\Users\Александр\Desktop\DnIT_Project

# Создайте миграцию для приложения directories
python manage.py makemigrations directories
```

### Что происходит при выполнении команды:

```
┌─────────────────────────────────────────────────────────┐
│                    makemigrations                       │
└─────────────────────────────────────────────────────────┘

1. Django сканирует models.py в приложении directories
         │
         │ Сравнивает с последним состоянием миграций
         ▼
2. Обнаруживает изменения:
   • Добавлено поле: organization_type
   • Изменено unique_together: добавлено organization_type
         │
         ▼
3. Создаёт файл миграции:
   apps/directories/migrations/000X_auto_20260317_XXXX.py
         │
         ▼
4. Выводит результат:

Migrations for 'directories':
  apps\directories\migrations\000X_auto_20260317_XXXX.py
    - Add field organization_type to contract
    - Add field organization_type to powerofattorney
    - Add field organization_type to worktype
    - Alter unique_together for contract (1 constraint(s))
    - Alter unique_together for powerofattorney (1 constraint(s))
```

### Что внутри файла миграции?

```python
# apps/directories/migrations/000X_auto_20260317_XXXX.py

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directories', '000X_previous_migration'),
    ]

    operations = [
        # 🔴 ДОБАВЛЕНИЕ ПОЛЯ organization_type В contract
        migrations.AddField(
            model_name='contract',
            name='organization_type',
            field=models.CharField(
                choices=[('GC', 'ГК (Группа компаний)'), 
                         ('CHOU', 'ЧОУ (Частное образовательное учреждение)')],
                max_length=10,
                verbose_name='Тип организации'
            ),
            # ⚠️ ВАЖНО: Значение по умолчанию для существующих записей
            # Но у нас записей нет, поэтому можно указать любое
            preserve_default=False,
        ),
        
        # 🔴 ИЗМЕНЕНИЕ unique_together В contract
        migrations.AlterUniqueTogether(
            name='contract',
            unique_together={('organization_type', 'number', 'date')},
        ),
        
        # 🔴 АНАЛОГИЧНЫЕ ОПЕРАЦИИ ДЛЯ powerofattorney И worktype
        migrations.AddField(
            model_name='powerofattorney',
            name='organization_type',
            field=models.CharField(
                choices=[('GC', 'ГК (Группа компаний)'), 
                         ('CHOU', 'ЧОУ (Частное образовательное учреждение)')],
                max_length=10,
                verbose_name='Тип организации'
            ),
        ),
        migrations.AlterUniqueTogether(
            name='powerofattorney',
            unique_together={('organization_type', 'number', 'date')},
        ),
        
        migrations.AddField(
            model_name='worktype',
            name='organization_type',
            field=models.CharField(
                choices=[('GC', 'ГК (Группа компаний)'), 
                         ('CHOU', 'ЧОУ (Частное образовательное учреждение)')],
                max_length=10,
                verbose_name='Тип организации'
            ),
        ),
    ]
```

### Шаг 2: Применение миграции

```bash
# Примените миграцию к базе данных
python manage.py migrate directories
```

### Что происходит при выполнении команды:

```
┌─────────────────────────────────────────────────────────┐
│                         migrate                         │
└─────────────────────────────────────────────────────────┘

1. Django читает файл миграции
         │
         ▼
2. Проверяет, какие миграции уже применены
   (таблица django_migrations в БД)
         │
         ▼
3. Применяет новые операции по порядку:
         
   ┌─────────────────────────────────────────────────────┐
   │ Операция 1: AddField (contract)                     │
   │                                                     │
   │ SQL: ALTER TABLE directories_contract               │
   │      ADD COLUMN organization_type VARCHAR(10)       │
   │      NOT NULL DEFAULT 'GC'                          │
   └─────────────────────────────────────────────────────┘
         │
         ▼
   ┌─────────────────────────────────────────────────────┐
   │ Операция 2: AlterUniqueTogether (contract)          │
   │                                                     │
   │ SQL: ALTER TABLE directories_contract               │
   │      DROP CONSTRAINT directories_contract_...       │
   │                                                     │
   │      ALTER TABLE directories_contract               │
   │      ADD CONSTRAINT directories_contract_...        │
   │      UNIQUE (organization_type, number, date)       │
   └─────────────────────────────────────────────────────┘
         │
         ▼
   ┌─────────────────────────────────────────────────────┐
   │ Операция 3-5: Аналогично для powerofattorney        │
   └─────────────────────────────────────────────────────┘
         │
         ▼
4. Записывает номер миграции в django_migrations
         │
         ▼
5. Выводит результат:

Operations to perform:
  Apply all migrations: directories
Running migrations:
  Applying directories.000X_auto_20260317_XXXX... OK
```

### Проверка результата:

```bash
# Войдите в оболочку Django
python manage.py shell
```

```python
# Проверьте, что поле добавлено
from apps.directories.models import Contract

# Создайте тестовый договор
contract = Contract(
    organization_type='GC',
    number='ТЕСТ/1',
    date='2026-01-12',
)

# Проверьте, что поле существует
print(contract.organization_type)  # → 'GC'

# Попробуйте сохранить
# contract.save()  # ← Если нет ошибок, всё работает!
```

### Выход из оболочки:

```python
exit()
```

---

## 🔄 Полный цикл работы

### Сценарий: Создание двух договоров с одинаковым номером и датой

```
┌─────────────────────────────────────────────────────────────────┐
│                    ПОЛНЫЙ ЦИКЛ СОЗДАНИЯ                         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ ЭТАП 1: Создание договора для ГК                                │
└─────────────────────────────────────────────────────────────────┘

1. Пользователь открывает URL: /directories/contracts/create/
         │
         ▼
2. View: contract_create(request)
   • Создаёт пустую форму: form = ContractForm()
   • organisation_type = None (нет значения по умолчанию)
         │
         ▼
3. Template: contract_form.html
   • Отображает форму с полем выбора организации
         │
         ▼
4. Пользователь заполняет форму:
   ┌─────────────────────────────────────┐
   │ Тип организации: [ГК ▼]             │
   │ Номер договора: [А/1]               │
   │ Дата: [12.01.2026]                  │
   │ Контрагент: [ООО "УК"]              │
   └─────────────────────────────────────┘
         │
         ▼
5. Пользователь нажимает "Сохранить"
   → POST-запрос на /directories/contracts/create/
         │
         ▼
6. View: contract_create(request)
   • Создаёт форму с данными: form = ContractForm(request.POST)
         │
         ▼
7. form.is_valid() → Запускается clean()
   • organization_type = 'GC'
   • number = 'А/1'
   • date = '2026-01-12'
         │
         ▼
8. Проверка в БД:
   SELECT COUNT(*) FROM directories_contract
   WHERE organization_type='GC' 
   AND number='А/1' 
   AND date='2026-01-12';
   
   Результат: 0 → Валидация пройдена ✓
         │
         ▼
9. form.save() → INSERT в БД
   INSERT INTO directories_contract 
   (organization_type, number, date, counterparty_id)
   VALUES ('GC', 'А/1', '2026-01-12', 5);
         │
         ▼
10. Перенаправление на /directories/contracts/
    → Сообщение: "Договор "А/1" успешно создан!"
         │
         ▼
11. Пользователь видит в списке:
    ┌────┬─────────────┬──────────┬────────────┬──────────────────┐
    │ id │ Организация │ Номер    │ Дата       │ Контрагент       │
    ├────┼─────────────┼──────────┼────────────┼──────────────────┤
    │ 1  │ [ГК]        │ А/1      │ 12.01.2026 │ ООО "УК"         │
    └────┴─────────────┴──────────┴────────────┴──────────────────┘


┌─────────────────────────────────────────────────────────────────┐
│ ЭТАП 2: Создание договора для ЧОУ с тем же номером и датой      │
└─────────────────────────────────────────────────────────────────┘

1. Пользователь открывает URL: /directories/contracts/create/
         │
         ▼
2. Пользователь заполняет форму:
   ┌─────────────────────────────────────┐
   │ Тип организации: [ЧОУ ▼]            │
   │ Номер договора: [А/1]               │
   │ Дата: [12.01.2026]                  │
   │ Контрагент: [ООО "УК"]              │
   └─────────────────────────────────────┘
         │
         ▼
3. POST-запрос → form.is_valid() → clean()
   • organization_type = 'CHOU'
   • number = 'А/1'
   • date = '2026-01-12'
         │
         ▼
4. Проверка в БД:
   SELECT COUNT(*) FROM directories_contract
   WHERE organization_type='CHOU' 
   AND number='А/1' 
   AND date='2026-01-12';
   
   Результат: 0 → Валидация пройдена ✓
         │
         ▼
5. form.save() → INSERT в БД
   INSERT INTO directories_contract 
   (organization_type, number, date, counterparty_id)
   VALUES ('CHOU', 'А/1', '2026-01-12', 5);
         │
         ▼
6. Перенаправление на /directories/contracts/
    → Сообщение: "Договор "А/1" успешно создан!"
         │
         ▼
7. Пользователь видит в списке:
    ┌────┬─────────────┬──────────┬────────────┬──────────────────┐
    │ id │ Организация │ Номер    │ Дата       │ Контрагент       │
    ├────┼─────────────┼──────────┼────────────┼──────────────────┤
    │ 1  │ [ГК]        │ А/1      │ 12.01.2026 │ ООО "УК"         │
    │ 2  │ [ЧОУ]       │ А/1      │ 12.01.2026 │ ООО "УК"         │ ← ✅ МОЖНО!
    └────┴─────────────┴──────────┴────────────┴──────────────────┘


┌─────────────────────────────────────────────────────────────────┐
│ ЭТАП 3: Попытка создать дубликат для ГК                         │
└─────────────────────────────────────────────────────────────────┘

1. Пользователь заполняет форму:
   ┌─────────────────────────────────────┐
   │ Тип организации: [ГК ▼]             │
   │ Номер договора: [А/1]               │
   │ Дата: [12.01.2026]                  │
   │ Контрагент: [ИП Петров]             │
   └─────────────────────────────────────┘
         │
         ▼
2. POST-запрос → form.is_valid() → clean()
         │
         ▼
3. Проверка в БД:
   SELECT COUNT(*) FROM directories_contract
   WHERE organization_type='GC' 
   AND number='А/1' 
   AND date='2026-01-12';
   
   Результат: 1 → Такая запись УЖЕ есть! (id=1)
         │
         ▼
4. form.add_error() → Добавляется ошибка:
   "Договор с номером "А/1" от 12.01.2026 уже существует для ГК (Группа компаний)."
         │
         ▼
5. Форма возвращается пользователю с ошибкой:
   ┌─────────────────────────────────────────────────────────┐
   │ Тип организации *                                       │
   │ ┌─────────────────────────────────────────────────────┐ │
   │ │ ГК (Группа компаний)                                ▼ │ │
   │ └─────────────────────────────────────────────────────┘ │
   │                                                         │
   │ Номер договора                                          │
   │ ┌─────────────────────────────────────────────────────┐ │
   │ │ А/1                                                 │ │
   │ └─────────────────────────────────────────────────────┘ │
   │                                                         │
   │ Дата договора                                           │
   │ ┌─────────────────────────────────────────────────────┐ │
   │ │ 12.01.2026                                          │ │
   │ └─────────────────────────────────────────────────────┘ │
   │                                                         │
   │ ⚠️ Договор с номером "А/1" от 12.01.2026 уже           │
   │    существует для ГК (Группа компаний).                 │
   └─────────────────────────────────────────────────────────┘
```

---

## ⚠️ Частые ошибки и как их избежать

### Ошибка 1: Забыли добавить поле в `fields`

```python
# ❌ НЕПРАВИЛЬНО
class ContractForm(forms.ModelForm):
    organization_type = forms.ChoiceField(...)
    
    class Meta:
        model = Contract
        fields = ['number', 'date', 'counterparty']  # ← НЕТ organization_type!

# ✅ ПРАВИЛЬНО
class ContractForm(forms.ModelForm):
    organization_type = forms.ChoiceField(...)
    
    class Meta:
        model = Contract
        fields = ['organization_type', 'number', 'date', 'counterparty']
```

**Симптом:** Поле не отображается в форме, данные не сохраняются.

---

### Ошибка 2: Добавили `default='GC'` в модель

```python
# ❌ НЕПРАВИЛЬНО
organization_type = models.CharField(
    max_length=10,
    choices=ORGANIZATION_TYPE_CHOICES,
    default='GC',  # ← Пользователь может забыть изменить!
    verbose_name="Тип организации"
)

# ✅ ПРАВИЛЬНО
organization_type = models.CharField(
    max_length=10,
    choices=ORGANIZATION_TYPE_CHOICES,
    # ← НЕТ default, чтобы пользователь ОБЯЗАТЕЛЬНО выбрал
    verbose_name="Тип организации"
)
```

**Симптом:** При создании договора по умолчанию выбирается 'GC', пользователь не замечает и сохраняет.

---

### Ошибка 3: Забыли изменить `unique_together`

```python
# ❌ НЕПРАВИЛЬНО
class Meta:
    unique_together = ['number', 'date']  # ← Старое значение!

# ✅ ПРАВИЛЬНО
class Meta:
    unique_together = ['organization_type', 'number', 'date']
```

**Симптом:** Ошибка уникальности при создании договоров для разных организаций.

---

### Ошибка 4: Забыли добавить индексы

```python
# ❌ НЕПРАВИЛЬНО
class Meta:
    unique_together = ['organization_type', 'number', 'date']
    # ← НЕТ indexes для organization_type

# ✅ ПРАВИЛЬНО
class Meta:
    unique_together = ['organization_type', 'number', 'date']
    indexes = [
        models.Index(fields=['organization_type']),  # ← Для быстрой фильтрации
        models.Index(fields=['number']),
        models.Index(fields=['date']),
    ]
```

**Симптом:** Медленная фильтрация по organization_type при большом количестве записей.

---

### Ошибка 5: Не добавили фильтрацию в views

```python
# ❌ НЕПРАВИЛЬНО
@login_required
def contract_list(request):
    contracts = Contract.objects.select_related('counterparty').all()
    # ← НЕТ фильтрации по org_type
    
    context = {
        'contracts': contracts,
        # ← НЕТ org_type в контексте
    }
    return render(request, 'directories/contract_list.html', context)

# ✅ ПРАВИЛЬНО
@login_required
def contract_list(request):
    contracts = Contract.objects.select_related('counterparty').all()
    
    org_type = request.GET.get('org_type', '')
    if org_type in ['GC', 'CHOU']:
        contracts = contracts.filter(organization_type=org_type)
    
    context = {
        'contracts': contracts,
        'org_type': org_type,  # Для кнопок фильтра
    }
    return render(request, 'directories/contract_list.html', context)
```

**Симптом:** Кнопки фильтра есть, но не работают.

---

### Ошибка 6: Забыли применить миграцию

```bash
# ❌ НЕПРАВИЛЬНО
# Изменили models.py → сразу запустили сервер

# ✅ ПРАВИЛЬНО
# Изменили models.py → makemigrations → migrate → запустили сервер
```

**Симптом:** Ошибка базы данных: "column organization_type does not exist".

---

## ✅ Контрольный список

### Перед началом работы:

- [ ] Сделайте резервную копию базы данных (если есть данные)
- [ ] Убедитесь, что все тестовые данные удалены
- [ ] Закройте все активные сессии Django

### Изменения в моделях:

- [ ] Добавлено `ORGANIZATION_TYPE_CHOICES` в `Contract`
- [ ] Добавлено поле `organization_type` в `Contract`
- [ ] Изменено `unique_together` в `Contract.Meta`
- [ ] Добавлены индексы для `organization_type` в `Contract`
- [ ] Те же изменения в `PowerOfAttorney`
- [ ] Те же изменения в `WorkType`

### Изменения в формах:

- [ ] Добавлено поле `organization_type` вручную в `ContractForm`
- [ ] Добавлено `organization_type` в `fields` в `Meta`
- [ ] Обновлён метод `__init__` для инициализации поля
- [ ] Обновлён метод `clean()` для проверки уникальности
- [ ] Те же изменения в `PowerOfAttorneyForm`
- [ ] Те же изменения в `WorkTypeForm`

### Изменения в шаблонах:

- [ ] Добавлено поле `organization_type` в `contract_form.html`
- [ ] Добавлены кнопки фильтра в `contract_list.html`
- [ ] Добавлено отображение бейджа организации в таблице
- [ ] Те же изменения в шаблонах для доверенностей и видов работ

### Изменения в views:

- [ ] Добавлена фильтрация по `org_type` в `contract_list`
- [ ] Добавлен `org_type` в контекст
- [ ] Те же изменения в `power_of_attorney_list` и `work_type_list`

### Миграции:

- [ ] Создана миграция: `python manage.py makemigrations directories`
- [ ] Применена миграция: `python manage.py migrate directories`
- [ ] Проверено, что миграция применилась без ошибок

### Тестирование:

- [ ] Создание договора для ГК
- [ ] Создание договора для ЧОУ с тем же номером и датой
- [ ] Попытка создать дубликат для ГК (должна быть ошибка)
- [ ] Фильтрация по кнопкам "Все", "ГК", "ЧОУ"
- [ ] Редактирование существующего договора
- [ ] Те же тесты для доверенностей и видов работ

---

## 📖 Приложение: Справочник терминов

### Django-термины:

| Термин | Описание |
|--------|----------|
| **Модель (Model)** | Python-класс, описывающий таблицу в базе данных |
| **Форма (Form)** | Класс для обработки пользовательского ввода |
| **ModelForm** | Форма, автоматически созданная на основе модели |
| **View (Представление)** | Функция, обрабатывающая HTTP-запрос и возвращающая ответ |
| **Template (Шаблон)** | HTML-файл с Django-тегами для динамического контента |
| **QuerySet** | "Ленивый" запрос к базе данных |
| **Миграция** | Файл с инструкциями по изменению структуры БД |
| **ORM** | Object-Relational Mapping — преобразование Python-кода в SQL |
| **Widget** | Класс, определяющий HTML-представление поля формы |
| **ChoiceField** | Поле формы с выпадающим списком вариантов |

### SQL-термины:

| Термин | Описание |
|--------|----------|
| **INSERT** | Добавление новой записи в таблицу |
| **SELECT** | Получение записей из таблицы |
| **UPDATE** | Обновление существующей записи |
| **DELETE** | Удаление записи из таблицы |
| **WHERE** | Условие для фильтрации записей |
| **UNIQUE** | Ограничение уникальности значений |
| **INDEX** | Индекс для ускорения поиска |
| **FOREIGN KEY** | Внешний ключ для связи между таблицами |
| **CONSTRAINT** | Ограничение целостности данных |

### HTML-термины:

| Термин | Описание |
|--------|----------|
| **`<form>`** | HTML-форма для отправки данных на сервер |
| **`<input>`** | Поле ввода (текст, дата, скрытое поле) |
| **`<select>`** | Выпадающий список вариантов |
| **`<option>`** | Вариант в выпадающем списке |
| **`<label>`** | Подпись к полю формы |
| **POST** | HTTP-метод для отправки данных на сервер |
| **GET** | HTTP-метод для получения данных (параметры в URL) |

---

## 📚 Дополнительные ресурсы

### Официальная документация Django:

- [Модели данных](https://docs.djangoproject.com/en/stable/topics/db/models/)
- [Формы Django](https://docs.djangoproject.com/en/stable/topics/forms/)
- [Представления (Views)](https://docs.djangoproject.com/en/stable/topics/http/views/)
- [Шаблоны Django](https://docs.djangoproject.com/en/stable/topics/templates/)
- [Миграции](https://docs.djangoproject.com/en/stable/topics/migrations/)

### Полезные статьи:

- [Django ModelForm](https://docs.djangoproject.com/en/stable/topics/forms/modelforms/)
- [Валидация форм](https://docs.djangoproject.com/en/stable/ref/forms/validation/)
- [QuerySet API](https://docs.djangoproject.com/en/stable/ref/models/querysets/)

---

## 🎉 Заключение

Поздравляем! Теперь вы понимаете, как реализовать разделение данных между двумя организациями в Django-приложении.

### Что вы изучили:

✅ Как добавить новое поле в модель Django  
✅ Как изменить уникальность записей в базе данных  
✅ Как создать форму с обязательным выбором значения  
✅ Как отобразить поле в HTML-шаблоне  
✅ Как фильтровать данные по выбранному значению  
✅ Как создавать и применять миграции  

### Следующие шаги:

1. Примените эти знания к вашему проекту
2. Протестируйте все сценарии использования
3. Убедитесь, что миграции применились без ошибок

Удачи в разработке! 🚀
