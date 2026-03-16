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

from apps.directories.models import Counterparty, WorkType, Unit

# Проверяем, что все три модели импортируются
print("✅ Модели справочников:")
print(f"  - {WorkType._meta.verbose_name}")
print(f"  - {Unit._meta.verbose_name}")
print(f"  - {Counterparty._meta.verbose_name}")

# Проверяем поля Counterparty
print("\n✅ Поля Counterparty:")
for field in Counterparty._meta.get_fields():
    if field.name in ['name', 'inn', 'kpp', 'email', 'phone', 'is_archived']:
        print(f"  - {field.name}")

# Проверяем индексы
print("\n✅ Индексы:")
for index in Counterparty._meta.indexes:
    print(f"  - {index.fields}")
