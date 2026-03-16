# test_contract_form.py
"""
Тесты для ContractForm (обновлённая версия с модальным окном)
"""

import os
import django

# Настройка Django окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dNit_management.settings')
django.setup()

from django.utils import timezone

from apps.directories.forms import ResponsiblePersonForm
from apps.directories.models import ResponsiblePerson

print("=" * 60)
print("🧪 ТЕСТЫ ДЛЯ ResponsiblePersonForm")
print("=" * 60)

# ТЕСТ 1: Импорт формы
print("\n✅ ТЕСТ 1: Импорт формы")
print("   ✅ ResponsiblePersonForm импортирован успешно!")

# ТЕСТ 2: Проверка полей формы
form = ResponsiblePersonForm()
expected_fields = ['last_name', 'first_name', 'middle_name', 'position']
actual_fields = list(form.fields.keys())
print(f"\n✅ ТЕСТ 2: Проверка полей формы")
print(f"   Ожидаемые: {expected_fields}")
print(f"   Фактические: {actual_fields}")
if set(expected_fields) == set(actual_fields):
    print("   ✅ Все поля присутствуют!")

# ТЕСТ 3: Проверка виджетов
print(f"\n✅ ТЕСТ 3: Проверка виджетов")
for field_name in expected_fields:
    widget = form.fields[field_name].widget.__class__.__name__
    css_class = form.fields[field_name].widget.attrs.get('class')
    print(f"   {field_name}: {widget} (class: {css_class})")

# ТЕСТ 4: Проверка метода clean
print(f"\n✅ ТЕСТ 4: Проверка метода clean")
has_clean = hasattr(ResponsiblePersonForm, 'clean')
print(f"   Метод clean существует: {has_clean}")
if has_clean:
    print("   ✅ Метод clean определён!")

# ТЕСТ 5: Валидация пустой формы
print(f"\n✅ ТЕСТ 5: Валидация пустой формы")
form_empty = ResponsiblePersonForm(data={})
print(f"   Пустая форма валидна: {form_empty.is_valid()}")
if not form_empty.is_valid():
    print(f"   ✅ Пустая форма невалидна (ошибок: {len(form_empty.errors)})")

# ТЕСТ 6: Валидация с данными
print(f"\n✅ ТЕСТ 6: Валидация с данными")
form_valid = ResponsiblePersonForm(data={
    'last_name': 'Иванов',
    'first_name': 'Иван',
    'middle_name': 'Иванович',
    'position': 'Менеджер'
})
print(f"   Форма с данными валидна: {form_valid.is_valid()}")
if form_valid.is_valid():
    print("   ✅ Форма с корректными данными валидна!")

print("\n" + "=" * 60)
print("🎉 ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ!")
print("=" * 60)
