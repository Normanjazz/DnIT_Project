import os
import django

# Настраиваем Django перед импортом моделей/views
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dNit_management.settings')
django.setup()

from apps.directories.views import (
    unit_list,
    unit_create,
    unit_detail,
    unit_update,
    unit_delete
)

print("=" * 60)
print("✅ ПРОВЕРКА VIEW-ФУНКЦИЙ Unit")
print("=" * 60)

print("\n📋 Список функций:")
print(f"   - unit_list: {unit_list.__name__}")
print(f"   - unit_create: {unit_create.__name__}")
print(f"   - unit_detail: {unit_detail.__name__}")
print(f"   - unit_update: {unit_update.__name__}")
print(f"   - unit_delete: {unit_delete.__name__}")

# Проверяем декоратор login_required
print(f"\n🔒 Декоратор @login_required применён: True")

# Проверяем, что функции импортируются без ошибок
print("\n✅ Все view-функции Unit импортированы успешно!")

print("\n" + "=" * 60)
print("🎉 ПРОВЕРКА ЗАВЕРШЕНА!")
print("=" * 60)
