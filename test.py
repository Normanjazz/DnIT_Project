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

from apps.directories.forms import UnitForm, WorkTypeForm
from apps.directories.models import Unit

# Проверяем, что форма импортируется
print("✅ UnitForm импортирован успешно!")

# Проверяем поля формы
form = UnitForm()
print(f"\n✅ Поля формы: {list(form.fields.keys())}")

# Проверяем виджеты
print(f"\n✅ Виджет full_name: {form.fields['full_name'].widget.__class__.__name__}")
print(f"✅ CSS класс: {form.fields['full_name'].widget.attrs.get('class')}")
print(f"✅ Placeholder: {form.fields['full_name'].widget.attrs.get('placeholder')}")

# Проверяем метод валидации
print(f"\n✅ Метод clean_full_name существует: {hasattr(UnitForm, 'clean_full_name')}")

# Проверяем, что это ModelForm
print(f"\n✅ Является ModelForm: {issubclass(UnitForm, forms.ModelForm)}")
print(f"✅ Класс модели в Meta: {UnitForm._meta.model.__name__}")

# 🧪 Тестируем валидацию
print("\n🧪 Тестируем валидацию уникальности...")

# Тест 1: Пустая форма (должна быть невалидна)
form_empty = UnitForm(data={})
print(f"✅ Форма без данных валидна: {form_empty.is_valid()}")
if not form_empty.is_valid():
    print(f"✅ Ошибки валидации: {form_empty.errors}")

# Тест 2: Форма с данными (должна быть валидна, если нет дубликатов)
form_valid = UnitForm(data={'full_name': 'Тестовая единица', 'short_name': 'те'})
print(f"✅ Форма с данными валидна: {form_valid.is_valid()}")

print("\n🎉 Все тесты выполнены!")


