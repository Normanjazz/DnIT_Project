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

from apps.directories.models import Contract, Counterparty

# Проверяем поля
print("✅ Поля Contract:")
for field in Contract._meta.get_fields():
    if field.name in ['number', 'date', 'counterparty', 'is_archived']:
        print(f"  - {field.name} ({field.__class__.__name__})")

# Проверяем связь
print("\n✅ Связь с Counterparty:")
print(f"  - counterparty ({Contract._meta.get_field('counterparty').__class__.__name__})")

# Проверяем unique_together
print("\n✅ Уникальность:")
print(f"  - {Contract._meta.unique_together}")