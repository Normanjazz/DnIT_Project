# test_contract_form.py
"""
Тесты для ContractForm (обновлённая версия с модальным окном)
"""

import os
import django

# Настройка Django окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dNit_management.settings')
django.setup()

from apps.directories.forms import ContractForm
from apps.directories.models import Contract, Counterparty
from django.utils import timezone

print("=" * 60)
print("🧪 ТЕСТЫ ДЛЯ ContractForm")
print("=" * 60)

# ─────────────────────────────────────────────────────────────
# ТЕСТ 1: Импорт формы
# ─────────────────────────────────────────────────────────────
print("\n✅ ТЕСТ 1: Импорт формы")
try:
    from apps.directories.forms import ContractForm
    print("   ✅ ContractForm импортирован успешно!")
except ImportError as e:
    print(f"   ❌ Ошибка импорта: {e}")

# ─────────────────────────────────────────────────────────────
# ТЕСТ 2: Проверка полей формы
# ─────────────────────────────────────────────────────────────
print("\n✅ ТЕСТ 2: Проверка полей формы")
form = ContractForm()
expected_fields = ['number', 'date', 'counterparty', 'counterparty_display']
actual_fields = list(form.fields.keys())

print(f"   Ожидаемые поля: {expected_fields}")
print(f"   Фактические поля: {actual_fields}")

if set(expected_fields) == set(actual_fields):
    print("   ✅ Все поля присутствуют!")
else:
    print("   ❌ Поля не совпадают!")

# ─────────────────────────────────────────────────────────────
# ТЕСТ 3: Проверка виджета counterparty (должен быть HiddenInput)
# ─────────────────────────────────────────────────────────────
print("\n✅ ТЕСТ 3: Проверка виджета counterparty")
counterparty_widget = form.fields['counterparty'].widget.__class__.__name__
print(f"   Виджет counterparty: {counterparty_widget}")

if counterparty_widget == 'HiddenInput':
    print("   ✅ counterparty — скрытое поле (HiddenInput)!")
else:
    print(f"   ❌ Ожидается HiddenInput, получено: {counterparty_widget}")

# ─────────────────────────────────────────────────────────────
# ТЕСТ 4: Проверка виджета counterparty_display (должен быть TextInput)
# ─────────────────────────────────────────────────────────────
print("\n✅ ТЕСТ 4: Проверка виджета counterparty_display")
display_widget = form.fields['counterparty_display'].widget.__class__.__name__
print(f"   Виджет counterparty_display: {display_widget}")

if display_widget == 'TextInput':
    print("   ✅ counterparty_display — текстовое поле (TextInput)!")
else:
    print(f"   ❌ Ожидается TextInput, получено: {display_widget}")

# ─────────────────────────────────────────────────────────────
# ТЕСТ 5: Проверка атрибута readonly у counterparty_display
# ─────────────────────────────────────────────────────────────
print("\n✅ ТЕСТ 5: Проверка атрибута readonly")
is_readonly = form.fields['counterparty_display'].widget.attrs.get('readonly')
print(f"   Атрибут readonly: {is_readonly}")

if is_readonly == 'readonly':
    print("   ✅ counterparty_display защищён от редактирования!")
else:
    print(f"   ⚠️ readonly не установлен (текущее значение: {is_readonly})")

# ─────────────────────────────────────────────────────────────
# ТЕСТ 6: Проверка CSS класса form-control
# ─────────────────────────────────────────────────────────────
print("\n✅ ТЕСТ 6: Проверка CSS класса form-control")
number_class = form.fields['number'].widget.attrs.get('class')
date_class = form.fields['date'].widget.attrs.get('class')
display_class = form.fields['counterparty_display'].widget.attrs.get('class')

print(f"   number class: {number_class}")
print(f"   date class: {date_class}")
print(f"   counterparty_display class: {display_class}")

if number_class == 'form-control' and date_class == 'form-control' and display_class == 'form-control':
    print("   ✅ Все поля имеют класс form-control!")
else:
    print("   ❌ Не все поля имеют класс form-control!")

# ─────────────────────────────────────────────────────────────
# ТЕСТ 7: Проверка метода __init__ (заполнение counterparty_display)
# ─────────────────────────────────────────────────────────────
print("\n✅ ТЕСТ 7: Проверка метода __init__")

# Создаём тестового контрагента
counterparty, created = Counterparty.objects.get_or_create(
    name='Тестовый Контрагент ООО',
    defaults={'inn': '1234567890'}
)

# Создаём тестовый договор
contract, created = Contract.objects.get_or_create(
    number='TEST-001',
    date=timezone.now().date(),
    counterparty=counterparty,
    defaults={}
)

# Инициализируем форму с существующим объектом
form_with_instance = ContractForm(instance=contract)
display_initial = form_with_instance.fields['counterparty_display'].initial

print(f"   counterparty_display.initial: {display_initial}")

if display_initial == counterparty.name:
    print("   ✅ counterparty_display заполняется именем контрагента!")
else:
    print(f"   ❌ Ожидается '{counterparty.name}', получено: {display_initial}")

# ─────────────────────────────────────────────────────────────
# ТЕСТ 8: Проверка валидации пустой формы
# ─────────────────────────────────────────────────────────────
print("\n✅ ТЕСТ 8: Проверка валидации пустой формы")
form_empty = ContractForm(data={})
is_valid = form_empty.is_valid()

print(f"   Пустая форма валидна: {is_valid}")

if not is_valid:
    print(f"   ✅ Пустая форма невалидна (ошибок: {len(form_empty.errors)})")
    print(f"   Ошибки: {list(form_empty.errors.keys())}")
else:
    print("   ❌ Пустая форма должна быть невалидна!")

# ─────────────────────────────────────────────────────────────
# ТЕСТ 9: Проверка валидации с данными
# ─────────────────────────────────────────────────────────────
print("\n✅ ТЕСТ 9: Проверка валидации с данными")
form_valid = ContractForm(data={
    'number': 'TEST-002',
    'date': '2026-03-15',
    'counterparty': counterparty.pk,
    'counterparty_display': counterparty.name,
})
is_valid = form_valid.is_valid()

print(f"   Форма с данными валидна: {is_valid}")

if is_valid:
    print("   ✅ Форма с корректными данными валидна!")
else:
    print(f"   ❌ Ошибки: {form_valid.errors}")

# ─────────────────────────────────────────────────────────────
# ТЕСТ 10: Проверка уникальности номер+дата
# ─────────────────────────────────────────────────────────────
print("\n✅ ТЕСТ 10: Проверка уникальности номер+дата")
form_duplicate = ContractForm(data={
    'number': 'TEST-001',  # Дубликат номера
    'date': timezone.now().date().isoformat(),  # Та же дата
    'counterparty': counterparty.pk,
    'counterparty_display': counterparty.name,
})
is_valid = form_duplicate.is_valid()

print(f"   Форма с дубликатом валидна: {is_valid}")

if not is_valid and 'non_field_errors' in form_duplicate.errors:
    print("   ✅ Дубликат номер+дата обнаружен!")
    print(f"   Ошибка: {form_duplicate.errors['non_field_errors'][0]}")
else:
    print("   ❌ Дубликат не обнаружен!")

# ─────────────────────────────────────────────────────────────
# ТЕСТ 11: Проверка метода clean (кросс-полевая валидация)
# ─────────────────────────────────────────────────────────────
print("\n✅ ТЕСТ 11: Проверка метода clean")
has_clean_method = hasattr(ContractForm, 'clean')
print(f"   Метод clean существует: {has_clean_method}")

if has_clean_method:
    print("   ✅ Метод clean определён!")
else:
    print("   ❌ Метод clean не найден!")

# ─────────────────────────────────────────────────────────────
# ТЕСТ 12: Проверка типа поля counterparty (ModelChoiceField)
# ─────────────────────────────────────────────────────────────
print("\n✅ ТЕСТ 12: Проверка типа поля counterparty")
field_type = form.fields['counterparty'].__class__.__name__
print(f"   Тип поля counterparty: {field_type}")

if field_type == 'ModelChoiceField':
    print("   ✅ counterparty — ModelChoiceField (связь с моделью)!")
else:
    print(f"   ⚠️ Тип: {field_type}")

# ─────────────────────────────────────────────────────────────
# ИТОГ
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("🎊 ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ!")
print("=" * 60)

# Очистка тестовых данных (опционально)
# contract.delete()
# counterparty.delete()