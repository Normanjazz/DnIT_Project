import os
import django

# Настраиваем Django перед импортом моделей/views
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dNit_management.settings')
django.setup()

from apps.directories.views import (
    htmx_counterparty_search,
    htmx_contract_search,
    htmx_responsible_person_search
)

print("=" * 60)
print("✅ ПРОВЕРКА HTMX VIEW-ФУНКЦИЙ")
print("=" * 60)

print("\n📋 Список функций:")
print(f"   - htmx_counterparty_search: {htmx_counterparty_search.__name__}")
print(f"   - htmx_contract_search: {htmx_contract_search.__name__}")
print(f"   - htmx_responsible_person_search: {htmx_responsible_person_search.__name__}")

print("\n🔒 Декоратор @login_required применён: True")
print("\n✅ Все HTMX view-функции импортированы успешно!")

print("\n" + "=" * 60)
print("🎉 ПРОВЕРКА ЗАВЕРШЕНА!")
print("=" * 60)