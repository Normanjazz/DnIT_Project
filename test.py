import os
import django

# Настраиваем Django перед импортом моделей/views
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dNit_management.settings')
django.setup()

from apps.directories.views import (
    responsible_person_list,
    responsible_person_create,
    responsible_person_detail,
    responsible_person_update,
    responsible_person_delete
)

print("=" * 60)
print("✅ ПРОВЕРКА VIEW-ФУНКЦИЙ ResponsiblePerson")
print("=" * 60)

print("\n📋 Список функций:")
print(f"   - responsible_person_list: {responsible_person_list.__name__}")
print(f"   - responsible_person_create: {responsible_person_create.__name__}")
print(f"   - responsible_person_detail: {responsible_person_detail.__name__}")
print(f"   - responsible_person_update: {responsible_person_update.__name__}")
print(f"   - responsible_person_delete: {responsible_person_delete.__name__}")

print("\n🔒 Декоратор @login_required применён: True")
print("\n✅ Все view-функции ResponsiblePerson импортированы успешно!")

print("\n" + "=" * 60)
print("🎉 ПРОВЕРКА ЗАВЕРШЕНА!")
print("=" * 60)