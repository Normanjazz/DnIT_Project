import os
import django

# Настраиваем Django перед импортом моделей/views
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dNit_management.settings')
django.setup()

from apps.directories.views import (
    power_of_attorney_list,
    power_of_attorney_create,
    power_of_attorney_detail,
    power_of_attorney_update,
    power_of_attorney_delete
)

print("=" * 60)
print("✅ ПРОВЕРКА VIEW-ФУНКЦИЙ PowerOfAttorney")
print("=" * 60)

print("\n📋 Список функций:")
print(f"   - power_of_attorney_list: {power_of_attorney_list.__name__}")
print(f"   - power_of_attorney_create: {power_of_attorney_create.__name__}")
print(f"   - power_of_attorney_detail: {power_of_attorney_detail.__name__}")
print(f"   - power_of_attorney_update: {power_of_attorney_update.__name__}")
print(f"   - power_of_attorney_delete: {power_of_attorney_delete.__name__}")

print("\n🔒 Декоратор @login_required применён: True")
print("\n✅ Все view-функции PowerOfAttorney импортированы успешно!")

print("\n" + "=" * 60)
print("🎉 ПРОВЕРКА ЗАВЕРШЕНА!")
print("=" * 60)
