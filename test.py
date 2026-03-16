import os
import sys
import django
from django.conf import settings

# Добавляем директорию проекта в путь Python
sys.path.append(os.path.join(os.path.dirname(__file__)))

# Устанавливаем переменную окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dNit_management.settings')

# Настройка Django
django.setup()

# Теперь можно безопасно импортировать модели
from apps.core.models import BaseModel

# --------- Вставляем код от QWEN ----------------------

from apps.directories.models import PowerOfAttorney, ResponsiblePerson

# Проверяем поля
print("✅ Поля PowerOfAttorney:")
for field in PowerOfAttorney._meta.get_fields():
    if field.name in ['number', 'date', 'responsible_person', 'is_archived']:
        print(f"  - {field.name} ({field.__class__.__name__})")

# Проверяем связь
print("\n✅ Связь с ResponsiblePerson:")
print(f"  - responsible_person ({PowerOfAttorney._meta.get_field('responsible_person').__class__.__name__})")

# Проверяем unique_together
print("\n✅ Уникальность:")
print(f"  - {PowerOfAttorney._meta.unique_together}")

# Проверяем related_name
print("\n✅ Обратная связь (related_name):")
print(f"  - {PowerOfAttorney._meta.get_field('responsible_person').remote_field.related_name}")

