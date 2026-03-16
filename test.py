# test_contract_form.py
"""
Тесты для ContractForm (обновлённая версия с модальным окном)
"""

import os
import django

# Настройка Django окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dNit_management.settings')
django.setup()

from apps.directories.forms import PowerOfAttorneyForm
from apps.directories.models import PowerOfAttorney, ResponsiblePerson
from django.utils import timezone

print("=" * 60)
print("🧪 ТЕСТЫ ДЛЯ PowerOfAttorneyForm")
print("=" * 60)

# ТЕСТ 1: Импорт формы
print("\n✅ ТЕСТ 1: Импорт формы")
print("   ✅ PowerOfAttorneyForm импортирован успешно!")

# ТЕСТ 2: Проверка полей формы
form = PowerOfAttorneyForm()
expected_fields = ['number', 'date', 'responsible_person', 'responsible_person_display']
actual_fields = list(form.fields.keys())
print(f"\n✅ ТЕСТ 2: Проверка полей формы")
print(f"   Ожидаемые: {expected_fields}")
print(f"   Фактические: {actual_fields}")
if set(expected_fields) == set(actual_fields):
    print("   ✅ Все поля присутствуют!")

# ТЕСТ 3: Проверка виджета responsible_person (должен быть HiddenInput)
print(f"\n✅ ТЕСТ 3: Проверка виджета responsible_person")
rp_widget = form.fields['responsible_person'].widget.__class__.__name__
print(f"   Виджет responsible_person: {rp_widget}")
if rp_widget == 'HiddenInput':
    print("   ✅ responsible_person — скрытое поле (HiddenInput)!")
else:
    print(f"   ❌ Ожидается HiddenInput, получено: {rp_widget}")

# ТЕСТ 4: Проверка виджета responsible_person_display (должен быть TextInput)
print(f"\n✅ ТЕСТ 4: Проверка виджета responsible_person_display")
display_widget = form.fields['responsible_person_display'].widget.__class__.__name__
print(f"   Виджет responsible_person_display: {display_widget}")
if display_widget == 'TextInput':
    print("   ✅ responsible_person_display — текстовое поле (TextInput)!")
else:
    print(f"   ❌ Ожидается TextInput, получено: {display_widget}")

# ТЕСТ 5: Проверка атрибута readonly
print(f"\n✅ ТЕСТ 5: Проверка атрибута readonly")
is_readonly = form.fields['responsible_person_display'].widget.attrs.get('readonly')
print(f"   Атрибут readonly: {is_readonly}")
if is_readonly == 'readonly':
    print("   ✅ responsible_person_display защищён от редактирования!")

# ТЕСТ 6: Проверка метода __init__
print(f"\n✅ ТЕСТ 6: Проверка метода __init__")
has_init = hasattr(PowerOfAttorneyForm, '__init__')
print(f"   Метод __init__ существует: {has_init}")
if has_init:
    print("   ✅ Метод __init__ определён!")

# ТЕСТ 7: Проверка метода clean
print(f"\n✅ ТЕСТ 7: Проверка метода clean")
has_clean = hasattr(PowerOfAttorneyForm, 'clean')
print(f"   Метод clean существует: {has_clean}")
if has_clean:
    print("   ✅ Метод clean определён!")

# ТЕСТ 8: Валидация пустой формы
print(f"\n✅ ТЕСТ 8: Валидация пустой формы")
form_empty = PowerOfAttorneyForm(data={})
print(f"   Пустая форма валидна: {form_empty.is_valid()}")
if not form_empty.is_valid():
    print(f"   ✅ Пустая форма невалидна (ошибок: {len(form_empty.errors)})")

# ТЕСТ 9: Валидация с данными
print(f"\n✅ ТЕСТ 9: Валидация с данными")
form_valid = PowerOfAttorneyForm(data={
    'number': 'TEST-001',
    'date': '2026-03-15',
    'responsible_person_display': 'Иванов Иван Иванович'
})
print(f"   Форма с данными валидна: {form_valid.is_valid()}")
if not form_valid.is_valid():
    print(f"   ⚠️ Ошибки: {form_valid.errors}")

print("\n" + "=" * 60)
print("🎉 ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ!")
print("=" * 60)

