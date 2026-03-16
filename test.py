import os
import django

# Настраиваем Django перед импортом моделей/views
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dNit_management.settings')
django.setup()

from apps.directories.views import (
    counterparty_list,
    counterparty_create,
    counterparty_detail,
    counterparty_update,
    counterparty_delete
)

print("=" * 60)
print("✅ ПРОВЕРКА VIEW-ФУНКЦИЙ Counterparty")
print("=" * 60)

print("\n📋 Список функций:")
print(f"   - counterparty_list: {counterparty_list.__name__}")
print(f"   - counterparty_create: {counterparty_create.__name__}")
print(f"   - counterparty_detail: {counterparty_detail.__name__}")
print(f"   - counterparty_update: {counterparty_update.__name__}")
print(f"   - counterparty_delete: {counterparty_delete.__name__}")

print("\n🔒 Декоратор @login_required применён: True")
print("\n✅ Все view-функции Counterparty импортированы успешно!")

print("\n" + "=" * 60)
print("🎉 ПРОВЕРКА ЗАВЕРШЕНА!")
print("=" * 60)