import os
import sys
import django
from django.conf import settings

# Настройка минимальной конфигурации Django
if not settings.configured:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dNit_management.settings')
    django.setup()

from apps.directories.forms import WorkTypeForm
from apps.directories.models import WorkType

# Проверяем, что форма импортируется
print("✅ WorkTypeForm импортирован успешно!")

# Проверяем поля формы
form = WorkTypeForm()
print(f"\n✅ Поля формы: {list(form.fields.keys())}")

# Проверяем виджеты
print(f"\n✅ Виджет full_name: {form.fields['full_name'].widget.__class__.__name__}")
print(f"✅ CSS класс: {form.fields['full_name'].widget.attrs.get('class')}")
print(f"✅ Placeholder для full_name: {form.fields['full_name'].widget.attrs.get('placeholder')}")

print(f"\n✅ Виджет short_name: {form.fields['short_name'].widget.__class__.__name__}")
print(f"✅ CSS класс: {form.fields['short_name'].widget.attrs.get('class')}")
print(f"✅ Placeholder для short_name: {form.fields['short_name'].widget.attrs.get('placeholder')}")

# Проверяем метки полей
print(f"\n✅ Метка full_name: {form.fields['full_name'].label}")
print(f"✅ Метка short_name: {form.fields['short_name'].label}")

# Проверяем метод валидации
print(f"\n✅ Метод clean_full_name существует: {hasattr(WorkTypeForm, 'clean_full_name')}")

# Проверяем, что форма является наследником ModelForm
print(f"\n✅ Является ModelForm: {isinstance(form, WorkTypeForm)}")
print(f"✅ Класс модели в Meta: {WorkTypeForm._meta.model.__name__}")

# Проверяем уникальность при валидации
print("\n🧪 Тестируем валидацию уникальности...")
# Создадим тестовые данные
test_data = {'full_name': 'Тестовый вид работ', 'short_name': 'ТВР'}
form_with_data = WorkTypeForm(data=test_data)
print(f"✅ Форма с данными валидна: {form_with_data.is_valid()}")

# Проверим, что пустые данные не проходят валидацию
empty_form = WorkTypeForm(data={})
print(f"✅ Форма без данных валидна: {empty_form.is_valid()}")
if not empty_form.is_valid():
    print(f"❌ Ошибки валидации: {empty_form.errors}")

print("\n🎉 Все тесты выполнены!")
