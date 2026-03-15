# scripts/init_folders.py
from pathlib import Path
from django.conf import settings

def create_folders():
    """Создаёт необходимую структуру папок для документов"""
    
    folders = [
        settings.FILES_STRUCTURE['bills'] / 'gc',
        settings.FILES_STRUCTURE['bills'] / 'chou',
        settings.FILES_STRUCTURE['reports'] / 'daily',
        settings.FILES_STRUCTURE['reports'] / 'weekly',
        settings.FILES_STRUCTURE['reports'] / 'in',
        settings.FILES_STRUCTURE['reports'] / 'avr',
        settings.FILES_STRUCTURE['protocols'],
    ]
    
    for folder in folders:
        folder.mkdir(parents=True, exist_ok=True)
        print(f"✓ Создана папка: {folder}")

if __name__ == '__main__':
    create_folders()