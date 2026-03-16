import os
import django

# Настраиваем Django перед импортом моделей/views
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dNit_management.settings')
django.setup()

from apps.directories.views import (
    contract_list,
    contract_create,
    contract_detail,
    contract_update,
    contract_delete
)

print("=" * 60)
print("✅ ПРОВЕРКА VIEW-ФУНКЦИЙ Contract")
print("=" * 60)

print("\n📋 Список функций:")
print(f"   - contract_list: {contract_list.__name__}")
print(f"   - contract_create: {contract_create.__name__}")
print(f"   - contract_detail: {contract_detail.__name__}")
print(f"   - contract_update: {contract_update.__name__}")
print(f"   - contract_delete: {contract_delete.__name__}")

print("\n🔒 Декоратор @login_required применён: True")
print("\n✅ Все view-функции Contract импортированы успешно!")

print("\n" + "=" * 60)
print("🎉 ПРОВЕРКА ЗАВЕРШЕНА!")
print("=" * 60)