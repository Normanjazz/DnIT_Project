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

from apps.directories.models import ResponsiblePerson, Contract

# Проверяем поля
print("✅ Поля ResponsiblePerson:")
for field in ResponsiblePerson._meta.get_fields():
    if field.name in ['last_name', 'first_name', 'middle_name', 'position', 'is_archived']:
        print(f"  - {field.name} ({field.__class__.__name__})")

# Проверяем __str__
print("\n✅ Проверка __str__:")
print(f"  - Метод __str__ определён: {hasattr(ResponsiblePerson, '__str__')}")