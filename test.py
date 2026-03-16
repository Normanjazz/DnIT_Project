import os
import sys
import django
from django.conf import settings
from django import forms

# Настройка минимальной конфигурации Django
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dNit_management.settings')
    django.setup()


# ============= от QWEN ==================

from apps.directories.forms import CounterpartyForm
from apps.directories.models import Counterparty

# Проверяем, что форма импортируется
print("✅ CounterpartyForm импортирован успешно!")

# Проверяем поля формы
form = CounterpartyForm()
print(f"\n✅ Поля формы: {list(form.fields.keys())}")

# Проверяем виджеты
print(f"\n✅ Виджет name: {form.fields['name'].widget.__class__.__name__}")
print(f"✅ Виджет email: {form.fields['email'].widget.__class__.__name__}")
print(f"✅ Виджет address: {form.fields['address'].widget.__class__.__name__}")

# Проверяем методы валидации
print(f"\n✅ Метод clean_name существует: {hasattr(CounterpartyForm, 'clean_name')}")
print(f"✅ Метод clean_inn существует: {hasattr(CounterpartyForm, 'clean_inn')}")
print(f"✅ Метод clean_kpp существует: {hasattr(CounterpartyForm, 'clean_kpp')}")

# 🧪 Тестируем валидацию ИНН
print("\n🧪 Тестируем валидацию ИНН...")

# Тест 1: Некорректный ИНН (5 цифр)
form_bad_inn = CounterpartyForm(data={
    'name': 'Тест ООО',
    'inn': '12345'
})
print(f"✅ Форма с ИНН '12345' валидна: {form_bad_inn.is_valid()}")
if not form_bad_inn.is_valid():
    print(f"✅ Ошибки: {form_bad_inn.errors.get('inn', 'Нет ошибок inn')}")

# Тест 2: Корректный ИНН (10 цифр)
form_good_inn = CounterpartyForm(data={
    'name': 'Тест ООО 2',
    'inn': '1234567890'
})
print(f"✅ Форма с ИНН '1234567890' валидна: {form_good_inn.is_valid()}")

# Тест 3: Корректный ИНН (12 цифр)
form_good_inn2 = CounterpartyForm(data={
    'name': 'Тест ООО 3',
    'inn': '123456789012'
})
print(f"✅ Форма с ИНН '123456789012' валидна: {form_good_inn2.is_valid()}")

print("\n🎉 Все тесты выполнены!")
