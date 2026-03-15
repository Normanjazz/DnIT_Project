## Веб-приложение "ДНиТ. Управление. Астрахань"
### Дата: 13.03.2026

---

# 📄 01_ОПИСАНИЕ_ПРИЛОЖЕНИЯ.md

## 1.1. Общие сведения

| Параметр | Значение |
|----------|----------|
| **Наименование системы** | ДНиТ. Управление. Астрахань |
| **Тип системы** | Веб-приложение для внутреннего использования (MPA) |
| **Назначение** | Автоматизация учёта счетов и формирования отчётной документации |
| **Количество пользователей** | 3-5 одновременных пользователей |
| **Объём данных** | До 50 записей в день (счета + отчёты) |
| **Среда развёртывания** | Выделенный ПК на Windows 10/11 во внутренней сети организации |
| **Авторизация** | Django Auth (django.contrib.auth), все пользователи имеют одинаковые права |

## 1.2. Цели и задачи системы

### Основные цели:
1. Централизованное хранение и учёт счетов на предоставление услуг
2. Автоматизация формирования отчётных документов по шаблонам (docxtpl + openpyxl)
3. Разделение данных по двум направлениям: ГК и ЧОУ
4. Минимизация ручного ввода данных через связанные справочники
5. Безопасное хранение конфигурации через `.env`

### Основные задачи:
- CRUD-операции со счетами (создание, чтение, обновление, удаление)
- Формирование счетов в формате MS Excel по шаблонам
- Генерация отчётов (ЕД, ЕН, ИН, заявки на акты) в MS Word
- Ведение справочников (договоры, контрагенты, виды работ, доверенности, ответственные лица)
- Пакетная обработка счетов (массовое формирование)
- Экспорт данных в Excel
- Мягкое удаление (Soft Delete) для всех сущностей

## 1.3. Функциональные области

```
┌─────────────────────────────────────────────────────────────────┐
│                    ДНиТ. Управление. Астрахань                   │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │     ГК      │  │    ЧОУ      │  │      СПРАВОЧНИКИ        │  │
│  │  (Группа    │  │  (Частное   │  │  - Виды работ           │  │
│  │   компаний) │  │   образов.  │  │  - Единицы измерения    │  │
│  │             │  │   учреждение)│  │  - Договоры             │  │
│  │  - Реестр   │  │  - Реестр   │  │  - Контрагенты          │  │
│  │    счетов   │  │    счетов   │  │  - Доверенности         │  │
│  │  - Отчёты   │  │  - Отчёты   │  │  - Ответственные лица   │  │
│  │  - Документы│  │  - Документы│  │                         │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────┐│
│  │          ПРОТОКОЛЫ И УДОСТОВЕРЕНИЯ (заглушка v1.0)          ││
│  │          - Загрузка Excel, выбор категории, выгрузка архива ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

## 1.4. Приоритеты разработки

| Приоритет | Модуль | Статус |
|-----------|--------|--------|
| **P0 (Критично)** | Авторизация и база пользователей | MVP |
| **P0 (Критично)** | Справочники (CRUD + Django Forms) | MVP |
| **P0 (Критично)** | Счета (CRUD + статусы + Django Forms) | MVP |
| **P1 (Важно)** | Реестры счетов (ГК/ЧОУ) | MVP |
| **P1 (Важно)** | Отчёты (ЕД, ЕН, ИН, Заявки) | MVP |
| **P2 (Средне)** | Генерация документов по шаблонам | После MVP |
| **P3 (Низко)** | Протоколы и удостоверения | Заглушка + v2.0 |

## 1.5. Ограничения системы

- Работа только во внутренней сети организации
- Отсутствие интеграции с внешними системами (1С, бухгалтерия и т.д.)
- Одиночная установка на одном сервере (без кластеризации)
- Максимум 50 записей в день
- Все пользователи имеют одинаковые права доступа
- Создание пользователей только через Django Admin

---

# 📄 02_ТЕХНИЧЕСКИЙ_СТЕК.md

## 2.1. Стек технологий

### Backend
| Компонент | Технология | Версия | Примечание |
|-----------|------------|--------|------------|
| Язык программирования | Python | 3.13+ | LTS версия |
| Веб-фреймворк | Django | 5.1+ | LTS версия |
| СУБД | PostgreSQL | 15+ | Основная БД |
| ORM | Django ORM | - | Встроенная |
| **Формы и валидация** | **Django Forms** | **встроенный** | **Без crispy-forms, ручная вёрстка** |
| **Переменные окружения** | **python-decouple** | **latest** | **Для .env файлов** |
| Шаблонизатор документов (Word) | docxtpl | latest | Для .docx |
| Шаблонизатор документов (Excel) | openpyxl | latest | Для .xlsx |
| WSGI-сервер | Waitress | latest | Для Windows |
| Автозапуск службы | NSSM | latest | Windows Service |

### Frontend
| Компонент | Технология | Версия | Примечание |
|-----------|------------|--------|------------|
| CSS-фреймворк | Bootstrap | 5.3+ | Адаптивная вёрстка |
| JavaScript | Vanilla JS | ES2024 | Без сборщиков, один файл на страницу |
| Интерактивность | Alpine.js | 3.x+ | Реактивность |
| Динамические запросы | HTMX | 1.9+ | AJAX без JS |
| Иконки | Bootstrap Icons | 1.11+ | Векторные иконки |

### Infrastructure
| Компонент | Технология | Версия | Примечание |
|-----------|------------|--------|------------|
| ОС сервера | Windows | 10/11 | Внутренняя сеть |
| Бэкап БД | Python + Task Scheduler | - | Ежедневно |
| SSL | Самоподписанный сертификат | - | Для Waitress |
| Конфигурация | .env файлы | - | SECRET_KEY, DB credentials |

## 2.2. Архитектурные принципы

```
┌─────────────────────────────────────────────────────────────────┐
│                         КЛИЕНТ (Браузер)                        │
│              (Bootstrap 5 + Alpine.js + HTMX + ES2024)          │
└─────────────────────────────────────────────────────────────────┘
                              │ HTTP/HTTPS
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    WAITRESS (WSGI Server)                       │
│                    (NSSM Auto-start + SSL)                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DJANGO 5.1 (MPA)                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │   Django    │  │   FBV       │  │   Django Templates      │  │
│  │   Auth      │  │   (Views)   │  │   (+ HTMX partials)     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
│  ┌─────────────┐  ┌─────────────┐                              │
│  │   Django    │  │   .env      │                              │
│  │   Forms     │  │   (decouple)│                              │
│  └─────────────┘  └─────────────┘                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    POSTGRESQL 15+                               │
│              (Django ORM + Soft Delete)                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    ФАЙЛОВОЕ ХРАНИЛИЩЕ                           │
│              D:/DnIT_Files/ (иерархия по датам)                 │
└─────────────────────────────────────────────────────────────────┘
```

## 2.3. Запрещённые технологии (для упрощения поддержки)

| Технология | Причина исключения | Альтернатива |
|------------|-------------------|--------------|
| Django REST Framework | Избыточно для MPA | Django Templates + HTMX |
| Class-Based Views (CBV) | Сложнее для понимания | Function-Based Views (FBV) |
| django-crispy-forms | Дополнительная абстракция | **Ручная вёрстка Django Forms** |
| Webpack/Vite | Избыточно для внутреннего приложения | Vanilla JS ES2024 |
| React/Vue | Избыточно для MPA | Alpine.js + HTMX |

## 2.4. Требования к окружению разработки

```bash
# Минимальные требования к ПК разработчика
- ОС: Windows 10/11 или Linux
- RAM: 8 ГБ минимум
- CPU: 4 ядра
- HDD: 10 ГБ свободного места
- Python: 3.13+
- PostgreSQL: 15+
- Git: latest
```

## 2.5. Безопасность конфигурации

### 2.5.1. Переменные окружения (.env)

| Требование | Описание |
|------------|----------|
| SECRET_KEY | Хранится только в `.env`, никогда в коде |
| DATABASE_URL | Подключение к PostgreSQL через переменную |
| DEBUG | Режим отладки через `.env` |
| .env в git | Добавлен в `.gitignore` |
| .env.example | Шаблон с заглушками в репозитории |

### 2.5.2. Пример .env файла

```env
# .env (не коммитить в git!)
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/dnit_db
ALLOWED_HOSTS=localhost,127.0.0.1,192.168.1.100

# Production
# SECRET_KEY=your-production-secret-key
# DEBUG=False
# ALLOWED_HOSTS=192.168.1.100
```

### 2.5.3. Пример .env.example

```env
# .env.example (можно коммитить)
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/your_db
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 2.5.4. Настройка settings.py

```python
from decouple import config, Csv

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

DATABASES = {
    'default': config('DATABASE_URL', cast=dj_database_url.parse)
}
```

---

# 📄 03_АРХИТЕКТУРА_ПРОЕКТА.md

## 3.1. Архитектурный стиль

**MPA (Multi-Page Application)** с элементами динамики через HTMX

### Почему MPA:
- Проще в разработке и поддержке
- Меньше JavaScript-кода
- Встроенная безопасность Django
- Лучшая SEO-индексируемость (не критично, но плюс)
- Быстрее разработка для команды из 1-2 разработчиков

## 3.2. Структура Django-приложений

```
dNit_management/
├── manage.py
├── requirements.txt
├── .env                      # Переменные окружения (НЕ в git)
├── .env.example              # Шаблон для разработчиков
├── .gitignore
├── dNit_management/          # Project settings
│   ├── __init__.py
│   ├── settings.py           # Настройки с config() из decouple
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── core/                 # Базовые абстракции, миксины
│   ├── accounts/             # Пользователи, авторизация
│   ├── bills/                # Счета (ГК + ЧОУ)
│   ├── reports/              # Отчёты (ЕД, ЕН, ИН, Заявки)
│   ├── directories/          # Справочники
│   └── protocols/            # Протоколы (заглушка v1.0)
├── templates/                # Глобальные шаблоны
│   ├── base.html
│   ├── components/
│   └── emails/
├── static/                   # Статика
│   ├── css/
│   ├── js/
│   └── img/
├── media/                    # Загружаемые файлы
├── files/                    # Сгенерированные документы
│   └── DnIT_Files/
├── scripts/                  # Скрипты (бэкап, миграции)
├── templates_doc/            # Шаблоны документов (Word/Excel)
└── docs/                     # Документация
```

## 3.3. Модульная структура

### App: `bills` (Счета)
```
bills/
├── __init__.py
├── models.py           # Bill, BillItem
├── views.py            # FBV для CRUD счетов
├── forms.py            # Django Forms (BillForm, BillItemFormSet)
├── urls.py             # /gc/bills/, /chou/bills/
├── templates/
│   └── bills/
│       ├── list.html
│       ├── detail.html
│       ├── form.html
│       └── _partials/  # HTMX partials
├── static/
│   └── bills/
│       └── js/
│           └── bill_form.js
└── services/
    └── bill_generator.py  # Генерация Excel
```

### App: `reports` (Отчёты)
```
reports/
├── __init__.py
├── models.py           # DailyReport, WeeklyReport, INReport, AVRRequest
├── views.py
├── forms.py            # Django Forms для отчётов
├── urls.py
├── templates/
│   └── reports/
└── services/
    └── report_generator.py  # Генерация Word
```

### App: `directories` (Справочники)
```
directories/
├── __init__.py
├── models.py           # WorkType, Unit, Contract, Counterparty, PowerOfAttorney, ResponsiblePerson
├── views.py
├── forms.py            # Django Forms для справочников
├── urls.py
└── templates/
    └── directories/
```

## 3.4. Схема взаимодействия компонентов

```
┌─────────────────────────────────────────────────────────────────┐
│                        ПОЛЬЗОВАТЕЛЬ                            │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼ HTTP Request
┌─────────────────────────────────────────────────────────────────┐
│                         URL Router                             │
│              (dNit_management/urls.py)                         │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Django View (FBV)                      │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │  1. Проверка авторизации (@login_required)              │   │
│   │  2. Валидация данных (Form.is_valid())                  │   │
│   │  3. Бизнес-логика (Service Layer)                       │   │
│   │  4. Сохранение в БД (Model.save())                      │   │
│   │  5. Генерация файла (при необходимости)                 │   │
│   │  6. Возврат TemplateResponse / HttpResponse             │   │
│   └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      PostgreSQL Database                       │
│              (Django ORM + Soft Delete)                        │
└─────────────────────────────────────────────────────────────────┘
```

## 3.5. Стратегия Soft Delete

Все модели наследуются от базового класса с полем `is_archived`:

```python
# apps/core/models.py
from django.db import models
from django.conf import settings

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_archived=False)

class BaseModel(models.Model):
    is_archived = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'accounts.User', 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='%(class)s_created'
    )
    
    objects = SoftDeleteManager()
    all_objects = models.Manager()
    
    class Meta:
        abstract = True
    
    def archive(self):
        self.is_archived = True
        self.save()
    
    def restore(self):
        self.is_archived = False
        self.save()
```

---

# 📄 04_СТРУКТУРА_ПАПОК.md

## 4.1. Полная структура проекта

```
D:/DnIT_Project/
│
├── 📁 dNit_management/                 # Django project
│   ├── __init__.py
│   ├── settings.py                     # Настройки проекта (с config())
│   ├── urls.py                         # Корневой URLconf
│   ├── wsgi.py                         # WSGI entry point
│   └── asgi.py
│
├── 📁 apps/                            # Django applications
│   ├── __init__.py
│   │
│   ├── 📁 core/                        # Базовые классы
│   │   ├── __init__.py
│   │   ├── models.py                   # BaseModel, миксины
│   │   ├── context_processors.py       # Глобальные переменные для шаблонов
│   │   └── templatetags/
│   │       └── custom_filters.py
│   │
│   ├── 📁 accounts/                    # Пользователи
│   │   ├── __init__.py
│   │   ├── models.py                   # User (расширение Django User)
│   │   ├── views.py
│   │   ├── forms.py                    # LoginForm, UserProfileForm
│   │   ├── urls.py
│   │   └── templates/
│   │       └── accounts/
│   │           ├── login.html
│   │           └── profile.html
│   │
│   ├── 📁 bills/                       # Счета
│   │   ├── __init__.py
│   │   ├── models.py                   # Bill, BillItem
│   │   ├── views.py
│   │   ├── forms.py                    # BillForm, BillItemFormSet
│   │   ├── urls.py                     # /gc/bills/, /chou/bills/
│   │   ├── templates/
│   │   │   └── bills/
│   │   │       ├── list.html
│   │   │       ├── form.html
│   │   │       ├── detail.html
│   │   │       └── _partials/
│   │   │           ├── bill_row.html
│   │   │           └── modal_contract.html
│   │   ├── static/
│   │   │   └── bills/
│   │   │       └── js/
│   │   │           └── bill_form.js
│   │   └── services/
│   │       └── bill_generator.py
│   │
│   ├── 📁 reports/                     # Отчёты
│   │   ├── __init__.py
│   │   ├── models.py                   # DailyReport, WeeklyReport, INReport, AVRRequest
│   │   ├── views.py
│   │   ├── forms.py                    # DailyReportForm, WeeklyReportForm, etc.
│   │   ├── urls.py
│   │   ├── templates/
│   │   │   └── reports/
│   │   │       ├── list.html
│   │   │       ├── form.html
│   │   │       └── _partials/
│   │   └── services/
│   │       └── report_generator.py
│   │
│   ├── 📁 directories/                 # Справочники
│   │   ├── __init__.py
│   │   ├── models.py                   # WorkType, Unit, Contract, Counterparty, PowerOfAttorney, ResponsiblePerson
│   │   ├── views.py
│   │   ├── forms.py                    # WorkTypeForm, UnitForm, ContractForm, etc.
│   │   ├── urls.py
│   │   └── templates/
│   │       └── directories/
│   │
│   └── 📁 protocols/                   # Протоколы (заглушка)
│       ├── __init__.py
│       ├── models.py                   # Заглушка
│       ├── views.py                    # Заглушка
│       ├── forms.py                    # Заглушка
│       ├── urls.py
│       └── templates/
│           └── protocols/
│
├── 📁 templates/                       # Глобальные шаблоны
│   ├── base.html                       # Базовый шаблон
│   ├── components/
│   │   ├── _navbar.html
│   │   ├── _sidebar.html
│   │   ├── _modal.html
│   │   └── _toast.html
│   └── emails/
│
├── 📁 static/                          # Статические файлы
│   ├── css/
│   │   ├── base.css
│   │   ├── components.css
│   │   └── utilities.css
│   ├── js/
│   │   ├── base.js
│   │   ├── htmx-config.js
│   │   └── alpine-init.js
│   └── img/
│       └── logo.png
│
├── 📁 media/                           # Загружаемые пользователем файлы
│   └── uploads/
│
├── 📁 files/                           # Сгенерированные документы
│   └── DnIT_Files/
│       ├── 📁 bills/
│       │   ├── 📁 2026/
│       │   │   ├── 📁 03/
│       │   │   └── 📁 04/
│       │   ├── 📁 gc/
│       │   └── 📁 chou/
│       ├── 📁 reports/
│       │   ├── 📁 daily/
│       │   ├── 📁 weekly/
│       │   ├── 📁 in/
│       │   └── 📁 avr/
│       └── 📁 protocols/
│
├── 📁 scripts/                         # Скрипты обслуживания
│   ├── backup_db.py                    # Бэкап БД
│   └── cleanup_temp.py                 # Очистка временных файлов
│
├── 📁 docs/                            # Документация
│   ├── README.md
│   ├── DEPLOYMENT.md
│   └── API.md
│
├── 📁 templates_doc/                   # Шаблоны документов (Word/Excel)
│   ├── bills/
│   │   ├── bill_template.xlsx
│   │   └── bill_offer_template.xlsx
│   └── reports/
│       ├── daily_report_template.docx
│       ├── weekly_report_template.docx
│       ├── in_report_template.docx
│       └── avr_request_template.docx
│
├── .env                                # Переменные окружения (НЕ в git)
├── .env.example                        # Шаблон для разработчиков
├── .gitignore
├── requirements.txt
├── manage.py
└── README.md
```

## 4.2. Структура базы данных PostgreSQL

```
dNit_db/
├── auth_user                           # Пользователи (Django Auth)
├── auth_group                          # Группы
├── auth_permission                     # Разрешения
├── django_content_type                 # Типы контента
├── django_session                      # Сессии
├── django_admin_log                    # Логи админки
│
├── directories_worktype                # Виды работ
├── directories_unit                    # Единицы измерения
├── directories_counterparty            # Контрагенты
├── directories_contract                # Договоры
├── directories_powerofattorney         # Доверенности
├── directories_responsibleperson       # Ответственные лица
│
├── bills_bill                          # Счета
├── bills_billitem                      # Позиции счетов
│
├── reports_dailyreport                 # Ежедневные отчёты
├── reports_weeklyreport                # Еженедельные отчёты
├── reports_inreport                    # ИН отчёты
└── reports_avrrequest                  # Заявки на акты
```

## 4.3. Конфигурация путей (settings.py)

```python
from pathlib import Path
from decouple import config, Csv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# Безопасность конфигурации
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

# Пути к приложениям
APPS_DIR = BASE_DIR / 'apps'

# Пути к файлам
MEDIA_ROOT = BASE_DIR / 'media'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Путь для сгенерированных документов (настраивается для prod)
FILES_ROOT = Path('D:/DnIT_Files')  # Production
# FILES_ROOT = BASE_DIR / 'files'   # Development

# Структура папок для документов
FILES_STRUCTURE = {
    'bills': FILES_ROOT / 'bills',
    'reports': FILES_ROOT / 'reports',
    'protocols': FILES_ROOT / 'protocols',
}

# Шаблоны документов
TEMPLATES_DOC_ROOT = BASE_DIR / 'templates_doc'

# Database
DATABASES = {
    'default': config('DATABASE_URL', cast=dj_database_url.parse)
}
```

---

# 📄 05_МОДЕЛИ_ДАННЫХ.md

## 5.1. Базовая модель (BaseModel)

```python
# apps/core/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone

class SoftDeleteManager(models.Manager):
    """Менеджер для мягкого удаления - скрывает архивированные записи"""
    def get_queryset(self):
        return super().get_queryset().filter(is_archived=False)

class BaseModel(models.Model):
    """Базовая модель с soft delete и аудитом"""
    
    is_archived = models.BooleanField(
        default=False, 
        db_index=True,
        verbose_name="Архивировано"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name="Дата изменения"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='%(class)s_created',
        verbose_name="Создал"
    )
    
    objects = SoftDeleteManager()
    all_objects = models.Manager()
    
    class Meta:
        abstract = True
        ordering = ['-created_at']
    
    def archive(self):
        """Мягкое удаление"""
        self.is_archived = True
        self.save(update_fields=['is_archived', 'updated_at'])
    
    def restore(self):
        """Восстановление из архива"""
        self.is_archived = False
        self.save(update_fields=['is_archived', 'updated_at'])
    
    def hard_delete(self):
        """Полное удаление (обход менеджера)"""
        self.all_objects.filter(pk=self.pk).delete()
```

## 5.2. Справочники (Directories)

### WorkType (Вид работ)
```python
class WorkType(BaseModel):
    full_name = models.CharField(
        max_length=500,
        verbose_name="Полное наименование"
    )
    short_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Сокращённое наименование"
    )
    
    class Meta:
        verbose_name = "Вид работ"
        verbose_name_plural = "Виды работ"
        ordering = ['full_name']
    
    def __str__(self):
        return self.full_name
```

### Unit (Единицы измерения)
```python
class Unit(BaseModel):
    full_name = models.CharField(
        max_length=100,
        verbose_name="Полное наименование"
    )
    short_name = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Сокращённое наименование"
    )
    
    class Meta:
        verbose_name = "Единица измерения"
        verbose_name_plural = "Единицы измерения"
        ordering = ['full_name']
    
    def __str__(self):
        return self.short_name or self.full_name
```

### Counterparty (Контрагент)
```python
class Counterparty(BaseModel):
    name = models.CharField(
        max_length=500,
        verbose_name="Наименование"
    )
    inn = models.CharField(
        max_length=12,
        blank=True,
        verbose_name="ИНН"
    )
    kpp = models.CharField(
        max_length=15,
        blank=True,
        verbose_name="КПП"
    )
    address = models.TextField(
        blank=True,
        verbose_name="Адрес"
    )
    email = models.EmailField(
        blank=True,
        verbose_name="E-mail"
    )
    phone = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Телефон"
    )
    
    class Meta:
        verbose_name = "Контрагент"
        verbose_name_plural = "Контрагенты"
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['inn']),
        ]
    
    def __str__(self):
        return self.name
```

### Contract (Договор)
```python
class Contract(BaseModel):
    number = models.CharField(
        max_length=100,
        verbose_name="Номер договора"
    )
    date = models.DateField(
        verbose_name="Дата договора"
    )
    counterparty = models.ForeignKey(
        Counterparty,
        on_delete=models.PROTECT,
        related_name='contracts',
        verbose_name="Контрагент"
    )
    
    class Meta:
        verbose_name = "Договор"
        verbose_name_plural = "Договоры"
        ordering = ['-date', 'number']
        unique_together = ['number', 'date']
        indexes = [
            models.Index(fields=['number']),
            models.Index(fields=['date']),
        ]
    
    def __str__(self):
        return f"{self.number} от {self.date.strftime('%d.%m.%Y')}"
```

### PowerOfAttorney (Доверенность)
```python
class PowerOfAttorney(BaseModel):
    number = models.CharField(
        max_length=50,
        verbose_name="Номер доверенности"
    )
    date = models.DateField(
        verbose_name="Дата доверенности"
    )
    responsible_person = models.ForeignKey(
        'ResponsiblePerson',
        on_delete=models.PROTECT,
        related_name='powers_of_attorney',
        verbose_name="Ответственное лицо"
    )
    
    class Meta:
        verbose_name = "Доверенность"
        verbose_name_plural = "Доверенности"
        ordering = ['-date', 'number']
        unique_together = ['number', 'date']
    
    def __str__(self):
        return f"№{self.number} от {self.date.strftime('%d.%m.%Y')}"
```

### ResponsiblePerson (Ответственное лицо)
```python
class ResponsiblePerson(BaseModel):
    last_name = models.CharField(
        max_length=100,
        verbose_name="Фамилия"
    )
    first_name = models.CharField(
        max_length=100,
        verbose_name="Имя"
    )
    middle_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Отчество"
    )
    position = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Должность"
    )
    
    class Meta:
        verbose_name = "Ответственное лицо"
        verbose_name_plural = "Ответственные лица"
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['last_name', 'first_name']),
        ]
    
    def __str__(self):
        full_name = f"{self.last_name} {self.first_name}"
        if self.middle_name:
            full_name += f" {self.middle_name}"
        return full_name
```

## 5.3. Счета (Bills)

### Bill (Счет)
```python
class Bill(BaseModel):
    ORGANIZATION_TYPE_CHOICES = [
        ('GC', 'ГК (Группа компаний)'),
        ('CHOU', 'ЧОУ (Частное образовательное учреждение)'),
    ]
    
    STATUS_CHOICES = [
        ('DRAFT', 'Черновик'),
        ('GENERATED', 'Сформирован'),
    ]
    
    # Организация
    organization_type = models.CharField(
        max_length=10,
        choices=ORGANIZATION_TYPE_CHOICES,
        default='GC',
        verbose_name="Тип организации"
    )
    
    # Основные поля
    number = models.CharField(
        max_length=50,
        verbose_name="Номер счета"
    )
    date = models.DateField(
        default=timezone.now,
        verbose_name="Дата счета"
    )
    is_offer = models.BooleanField(
        default=False,
        verbose_name="Оферта"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='DRAFT',
        verbose_name="Статус"
    )
    
    # Связанные сущности
    contract = models.ForeignKey(
        Contract,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='bills',
        verbose_name="Договор"
    )
    counterparty = models.ForeignKey(
        Counterparty,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='bills',
        verbose_name="Контрагент"
    )
    power_of_attorney = models.ForeignKey(
        PowerOfAttorney,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='bills',
        verbose_name="Доверенность"
    )
    
    # Связи с отчётами (nullable, one-to-many from report side)
    ed_report = models.ForeignKey(
        'reports.DailyReport',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bills',
        verbose_name="Ежедневный отчёт"
    )
    en_report = models.ForeignKey(
        'reports.WeeklyReport',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bills',
        verbose_name="Еженедельный отчёт"
    )
    in_report = models.ForeignKey(
        'reports.INReport',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bills',
        verbose_name="ИН отчёт"
    )
    avr_request = models.ForeignKey(
        'reports.AVRRequest',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bills',
        verbose_name="Заявка на акт"
    )
    
    class Meta:
        verbose_name = "Счет"
        verbose_name_plural = "Счета"
        ordering = ['-date', 'number']
        unique_together = ['organization_type', 'number']
        indexes = [
            models.Index(fields=['organization_type', 'status']),
            models.Index(fields=['date']),
            models.Index(fields=['is_offer']),
        ]
    
    def __str__(self):
        return f"Счет №{self.number} от {self.date.strftime('%d.%m.%Y')}"
    
    @property
    def total_amount(self):
        """Общая сумма по счету"""
        return sum(item.total for item in self.items.all())
    
    @property
    def is_locked(self):
        """Проверка блокировки счёта"""
        return bool(
            self.ed_report_id or 
            self.en_report_id or 
            self.in_report_id or 
            self.avr_request_id
        )
    
    def can_reset_status(self):
        """Можно ли сбросить статус 'Сформирован'"""
        return not self.is_locked
```

### BillItem (Позиция счета)
```python
class BillItem(BaseModel):
    bill = models.ForeignKey(
        Bill,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="Счет"
    )
    work_type = models.ForeignKey(
        WorkType,
        on_delete=models.PROTECT,
        related_name='bill_items',
        verbose_name="Вид работ"
    )
    description = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Дополнительные сведения"
    )
    unit = models.ForeignKey(
        Unit,
        on_delete=models.PROTECT,
        related_name='bill_items',
        verbose_name="Единица измерения"
    )
    quantity = models.DecimalField(
        max_digits=15,
        decimal_places=3,
        verbose_name="Количество"
    )
    price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Цена за единицу"
    )
    
    class Meta:
        verbose_name = "Позиция счета"
        verbose_name_plural = "Позиции счетов"
        ordering = ['id']
    
    def __str__(self):
        return f"{self.work_type} - {self.quantity} {self.unit}"
    
    @property
    def total(self):
        """Сумма по позиции"""
        return self.quantity * self.price
```

## 5.4. Отчёты (Reports)

### DailyReport (Ежедневный отчёт)
```python
class DailyReport(BaseModel):
    number = models.CharField(
        max_length=50,
        verbose_name="Номер отчёта"
    )
    date = models.DateField(
        verbose_name="Дата отчёта"
    )
    
    class Meta:
        verbose_name = "Ежедневный отчёт"
        verbose_name_plural = "Ежедневные отчёты"
        ordering = ['-date', 'number']
        unique_together = ['number', 'date']
    
    def __str__(self):
        return f"ЕД Отчёт №{self.number} от {self.date.strftime('%d.%m.%Y')}"
```

### WeeklyReport (Еженедельный отчёт)
```python
class WeeklyReport(BaseModel):
    number = models.CharField(
        max_length=50,
        verbose_name="Номер отчёта"
    )
    date_start = models.DateField(
        verbose_name="Дата начала периода"
    )
    date_end = models.DateField(
        verbose_name="Дата окончания периода"
    )
    
    class Meta:
        verbose_name = "Еженедельный отчёт"
        verbose_name_plural = "Еженедельные отчёты"
        ordering = ['-date_end', 'number']
    
    def __str__(self):
        return f"ЕН Отчёт №{self.number} ({self.date_start.strftime('%d.%m')} - {self.date_end.strftime('%d.%m.%Y')})"
```

### INReport (ИН отчёт)
```python
class INReport(BaseModel):
    number = models.CharField(
        max_length=50,
        verbose_name="Номер отчёта"
    )
    date = models.DateField(
        verbose_name="Дата отчёта"
    )
    
    class Meta:
        verbose_name = "ИН Отчёт"
        verbose_name_plural = "ИН Отчёты"
        ordering = ['-date', 'number']
    
    def __str__(self):
        return f"ИН Отчёт №{self.number} от {self.date.strftime('%d.%m.%Y')}"
```

### AVRRequest (Заявка на акт выполненных работ)
```python
class AVRRequest(BaseModel):
    number = models.CharField(
        max_length=50,
        verbose_name="Номер заявки"
    )
    date = models.DateField(
        verbose_name="Дата заявки"
    )
    
    class Meta:
        verbose_name = "Заявка на АВР"
        verbose_name_plural = "Заявки на АВР"
        ordering = ['-date', 'number']
    
    def __str__(self):
        return f"Заявка на АВР №{self.number} от {self.date.strftime('%d.%m.%Y')}"
```

## 5.5. ER-диаграмма

```
┌──────────────────────┐         ┌──────────────────────┐
│   Counterparty       │         │   ResponsiblePerson  │
│──────────────────────│         │──────────────────────│
│ id (PK)              │         │ id (PK)              │
│ name                 │         │ last_name            │
│ inn                  │         │ first_name           │
│ kpp                  │         │ middle_name          │
│ address              │         │ position             │
│ email                │         │ is_archived          │
│ phone                │         └──────────┬───────────┘
│ is_archived          │                    │
└──────────┬───────────┘                    │
           │ 1                              │ 1
           │                                │
           │ N                              │ N
┌──────────▼───────────┐         ┌──────────▼───────────┐
│   Contract           │         │   PowerOfAttorney    │
│──────────────────────│         │──────────────────────│
│ id (PK)              │         │ id (PK)              │
│ number               │         │ number               │
│ date                 │         │ date                 │
│ counterparty_id (FK) │         │ responsible_person_id│
│ is_archived          │         │ is_archived          │
└──────────┬───────────┘         └──────────┬───────────┘
           │ 1                              │ 1
           │                                │
           │ N                              │ N
           │                                │
┌──────────▼────────────────────────────────▼───────────┐
│                      Bill                             │
│───────────────────────────────────────────────────────│
│ id (PK)                                               │
│ organization_type (GC/CHOU)                           │
│ number                                                │
│ date                                                  │
│ is_offer                                              │
│ status (DRAFT/GENERATED)                              │
│ contract_id (FK, nullable)                            │
│ counterparty_id (FK, nullable)                        │
│ power_of_attorney_id (FK, nullable)                   │
│ ed_report_id (FK, nullable)                           │
│ en_report_id (FK, nullable)                           │
│ in_report_id (FK, nullable)                           │
│ avr_request_id (FK, nullable)                         │
│ is_archived                                           │
│ created_at, updated_at, created_by                    │
└───────────────────────┬───────────────────────────────┘
                        │ 1
                        │
                        │ N
┌───────────────────────▼───────────────────────────────┐
│                    BillItem                           │
│───────────────────────────────────────────────────────│
│ id (PK)                                               │
│ bill_id (FK)                                          │
│ work_type_id (FK)                                     │
│ description                                           │
│ unit_id (FK)                                          │
│ quantity                                              │
│ price                                                 │
│ is_archived                                           │
└───────────────────────────────────────────────────────┘

┌──────────────────────┐         ┌──────────────────────┐
│   WorkType           │         │   Unit               │
│──────────────────────│         │──────────────────────│
│ id (PK)              │         │ id (PK)              │
│ full_name            │         │ full_name            │
│ short_name           │         │ short_name           │
│ is_archived          │         │ is_archived          │
└──────────┬───────────┘         └──────────┬───────────┘
           │ 1                              │ 1
           │                                │
           │ N                              │ N
           └────────────────┬───────────────┘
                            │
                    ┌───────▼───────┐
                    │   BillItem    │
                    └───────────────┘

┌──────────────────────┐         ┌──────────────────────┐
│   DailyReport        │◄────────│   Bill (ed_report)   │
│──────────────────────│         └──────────────────────┘
│ id (PK)              │
│ number               │         ┌──────────────────────┐
│ date                 │         │   WeeklyReport       │◄────
│ is_archived          │         │──────────────────────│      │
└──────────────────────┘         │ id (PK)              │      │
                                 │ number               │      │
┌──────────────────────┐         │ date_start, date_end │      │
│   INReport           │◄────────│ is_archived          │      │
│──────────────────────│         └──────────────────────┘      │
│ id (PK)              │                                       │
│ number               │         ┌──────────────────────┐      │
│ date                 │         │   INReport           │◄─────┤
│ is_archived          │         │──────────────────────│      │
└──────────────────────┘         │ id (PK)              │      │
                                 │ number               │      │
┌──────────────────────┐         │ date                 │      │
│   AVRRequest         │◄────────│ is_archived          │      │
│──────────────────────│         └──────────────────────┘      │
│ id (PK)              │                                       │
│ number               │         ┌──────────────────────┐      │
│ date                 │         │   AVRRequest         │◄─────┘
│ is_archived          │         │──────────────────────│
└──────────────────────┘         │ id (PK)              │
                                 │ number               │
                                 │ date                 │
                                 │ is_archived          │
                                 └──────────────────────┘
```

---

# 📄 06_ПОЛЬЗОВАТЕЛЬСКИЕ_СЦЕНАРИИ.md

## 6.1. Роли пользователей

| Роль | Описание | Права |
|------|----------|-------|
| **Пользователь** | Основной пользователь системы | Полный доступ ко всем функциям |
| **Администратор** | Технический администратор | Доступ к Django Admin, управление пользователями |

> ⚠️ **Примечание**: В текущей версии все пользователи имеют одинаковые права. Разграничение прав не требуется. Создание пользователей только через Django Admin.

## 6.2. Сценарии использования

### UC-01: Авторизация в системе

```
┌─────────────────────────────────────────────────────────────────┐
│ АКТЁР: Пользователь                                             │
│ ПРЕДУСЛОВИЕ: Пользователь не авторизован                        │
│ ПОСТУСЛОВИЕ: Пользователь авторизован и перенаправлен на главную│
└─────────────────────────────────────────────────────────────────┘

1. Пользователь открывает URL приложения
2. Система перенаправляет на страницу входа (/accounts/login/)
3. Пользователь вводит логин и пароль (Django Auth Form)
4. Пользователь нажимает кнопку "Войти"
5. Система проверяет учётные данные
   ├── [5a] Учётные данные верны → Переход к шагу 6
   └── [5b] Учётные данные неверны → Показать ошибку, возврат к шагу 3
6. Система создаёт сессию пользователя
7. Система перенаправляет на главную страницу (/)
8. Конец
```

### UC-02: Создание нового счета (с Django Forms)

```
┌─────────────────────────────────────────────────────────────────┐
│ АКТЁР: Пользователь                                             │
│ ПРЕДУСЛОВИЕ: Пользователь авторизован, справочники заполнены    │
│ ПОСТУСЛОВИЕ: Счет создан в статусе "Черновик"                   │
└─────────────────────────────────────────────────────────────────┘

1. Пользователь переходит в раздел ГК или ЧОУ
2. Пользователь нажимает кнопку "Реестр счетов"
3. Пользователь нажимает кнопку "Создать счет"
4. Система открывает форму создания счета (BillForm + FormSet)
5. Пользователь заполняет поля:
   - Номер счета (вручную, валидация уникальности)
   - Дата счета (по умолчанию текущая)
   - Чекбокс "Оферта" (при необходимости)
   - Выбор договора ИЛИ выбор контрагента (в зависимости от оферты)
   - Добавление позиций счета (вид работ, количество, цена)
   - Выбор доверенности
6. Система валидирует данные через Django Forms
   ├── [6a] Ошибки валидации → Показать ошибки, возврат к шагу 5
   └── [6b] Данные валидны → Переход к шагу 7
7. Пользователь нажимает кнопку "Сохранить"
8. Система сохраняет счет в статусе "Черновик"
9. Система перенаправляет на страницу реестра счетов
10. Конец
```

### UC-03: Формирование счета (Excel)

```
┌─────────────────────────────────────────────────────────────────┐
│ АКТЁР: Пользователь                                             │
│ ПРЕДУСЛОВИЕ: Счет создан в статусе "Черновик", все поля заполнены│
│ ПОСТУСЛОВИЕ: Счет в статусе "Сформирован", файл Excel скачан    │
└─────────────────────────────────────────────────────────────────┘

1. Пользователь открывает форму редактирования счета
2. Система проверяет заполненность обязательных полей (Form.is_valid())
   ├── [2a] Есть незаполненные обязательные поля → Показать предупреждение
   └── [2b] Все поля заполнены → Переход к шагу 3
3. Пользователь нажимает кнопку "Сформировать"
4. Система определяет тип счета:
   ├── [4a] Оферта → Использовать шаблон bill_offer_template.xlsx
   └── [4b] Не оферта → Использовать шаблон bill_template.xlsx
5. Система генерирует Excel-файл через openpyxl
6. Система обновляет статус счета на "Сформирован"
7. Система сохраняет файл в D:/DnIT_Files/bills/{год}/{месяц}/
8. Система инициирует скачивание файла
9. Конец
```

### UC-04: Пакетное формирование счетов

```
┌─────────────────────────────────────────────────────────────────┐
│ АКТЁР: Пользователь                                             │
│ ПРЕДУСЛОВИЕ: В реестре есть несколько счетов в статусе "Черновик"│
│ ПОСТУСЛОВИЕ: Выбранные счета в статусе "Сформирован", архив скачан│
└─────────────────────────────────────────────────────────────────┘

1. Пользователь переходит на страницу реестра счетов
2. Пользователь отмечает чекбоксами счета для формирования
3. Пользователь нажимает кнопку "Сформировать выбранные"
4. Система проверяет каждый выбранный счет на заполненность
5. Для каждого счета:
   ├── [5a] Все поля заполнены → Генерация файла, статус "Сформирован"
   └── [5b] Есть незаполненные поля → Пропуск, запись в лог ошибок
6. Система создаёт ZIP-архив с успешными файлами
7. Система добавляет в архив файл log_errors.txt со списком ошибок
8. Система инициирует скачивание архива
9. Система показывает уведомление с результатами:
   - Успешно: X счетов
   - Ошибки: Y счетов (см. лог в архиве)
10. Конец
```

### UC-05: Создание ежедневного отчёта

```
┌─────────────────────────────────────────────────────────────────┐
│ АКТЁР: Пользователь                                             │
│ ПРЕДУСЛОВИЕ: Есть счета в статусе "Сформирован"                 │
│ ПОСТУСЛОВИЕ: Отчёт создан, файл Word скачан                     │
└─────────────────────────────────────────────────────────────────┘

1. Пользователь переходит в раздел "Ежедневные отчёты"
2. Пользователь нажимает кнопку "Создать отчёт"
3. Система открывает форму создания отчёта (DailyReportForm)
4. Пользователь заполняет:
   - Номер отчёта (авто: последний + 1)
   - Дата отчёта (по умолчанию текущая)
5. Система отображает список счетов со статусом "Сформирован"
6. Пользователь отмечает чекбоксами счета для включения в отчёт
7. Пользователь нажимает кнопку "Сформировать"
8. Система генерирует Word-файл через docxtpl
9. Система обновляет поле ed_report у выбранных счетов
10. Система сохраняет файл в D:/DnIT_Files/reports/daily/{год}/{месяц}/
11. Система инициирует скачивание файла
12. Конец
```

### UC-06: Выбор связанной сущности (модальное окно)

```
┌─────────────────────────────────────────────────────────────────┐
│ АКТЁР: Пользователь                                             │
│ ПРЕДУСЛОВИЕ: Пользователь редактирует счет                      │
│ ПОСТУСЛОВИЕ: Сущность выбрана и отображена в поле               │
└─────────────────────────────────────────────────────────────────┘

1. Пользователь нажимает кнопку "Выбрать" у поля (Договор/Контрагент/и т.д.)
2. Система открывает модальное окно через HTMX
3. Система загружает список сущностей (с пагинацией)
4. Пользователь вводит текст в поле поиска
5. Система фильтрует список в реальном времени (HTMX hx-trigger="keyup changed delay:300ms")
6. Пользователь выбирает сущность из списка
7. Пользователь нажимает кнопку "Выбрать" в модальном окне
   └── [7a] Альтернатива: Клик по строке сущности
8. Система закрывает модальное окно
9. Система заполняет поле выбранным значением
10. Конец

[Альтернативный поток: Создание новой сущности]
11. Пользователь нажимает кнопку "Добавить новую"
12. Система открывает форму создания в модальном окне (Django Form)
13. Пользователь заполняет поля и нажимает "Сохранить"
14. Система создаёт сущность и выбирает её автоматически
15. Возврат к шагу 8
```

### UC-07: Сброс статуса "Сформирован"

```
┌─────────────────────────────────────────────────────────────────┐
│ АКТЁР: Пользователь                                             │
│ ПРЕДУСЛОВИЕ: Счет в статусе "Сформирован"                       │
│ ПОСТУСЛОВИЕ: Статус сброшен на "Черновик" ИЛИ операция отклонена│
└─────────────────────────────────────────────────────────────────┘

1. Пользователь открывает форму редактирования счета
2. Система проверяет поле is_locked:
   ├── [2a] Счет заблокирован (участвует в отчётах) → Переход к шагу 3
   └── [2b] Счет не заблокирован → Переход к шагу 5
3. Система отображает UI-элемент со списком отчётов, где используется счет
4. Система блокирует кнопку сброса статуса → Конец
5. Пользователь нажимает красную кнопку "X" (сброс статуса)
6. Система показывает подтверждение действия
   ├── [6a] Пользователь отменил → Конец
   └── [6b] Пользователь подтвердил → Переход к шагу 7
7. Система обновляет статус на "Черновик"
8. Система показывает уведомление об успехе
9. Конец
```

### UC-08: Просмотр участия счета в отчётах

```
┌─────────────────────────────────────────────────────────────────┐
│ АКТЁР: Пользователь                                             │
│ ПРЕДУСЛОВИЕ: Счет открыт на просмотр/редактирование             │
│ ПОСТУСЛОВИЕ: Пользователь видит список отчётов со ссылками      │
└─────────────────────────────────────────────────────────────────┘

1. Система проверяет связи счета с отчётами
2. Если есть связи, система отображает UI-блок "Участие в отчётах":
   ┌─────────────────────────────────────────────────────┐
   │ 📋 Участие в отчётах                                │
   │ ├── 📄 Ежедневный отчёт №5 от 15.01.2026 [Перейти]  │
   │ ├── 📄 Еженедельный отчёт №2 от 10-16.01.2026 [Перейти]│
   │ └── 📄 Заявка на АВР №1 от 20.01.2026 [Перейти]     │
   └─────────────────────────────────────────────────────┘
3. Пользователь может кликнуть на ссылку для перехода к отчёту
4. Конец
```

### UC-09: Экспорт реестра в Excel

```
┌─────────────────────────────────────────────────────────────────┐
│ АКТЁР: Пользователь                                             │
│ ПРЕДУСЛОВИЕ: Пользователь находится на странице реестра счетов  │
│ ПОСТУСЛОВИЕ: Файл Excel со списком счетов скачан                │
└─────────────────────────────────────────────────────────────────┘

1. Пользователь применяет фильтры к реестру (при необходимости)
2. Пользователь нажимает кнопку "Экспорт в Excel"
3. Система генерирует Excel-файл с текущими данными реестра
4. Система инициирует скачивание файла
5. Конец
```

### UC-10: Формирование протоколов (заглушка v1.0)

```
┌─────────────────────────────────────────────────────────────────┐
│ АКТЁР: Пользователь                                             │
│ ПРЕДУСЛОВИЕ: Пользователь имеет Excel-файл с данными            │
│ ПОСТУСЛОВИЕ: Архив с документами скачан ИЛИ показано сообщение  │
└─────────────────────────────────────────────────────────────────┘

1. Пользователь переходит в раздел "Протоколы и удостоверения"
2. Система отображает форму с полями:
   - Загрузка Excel-файла
   - Выбор категории (Высота / ТБ / ЗП)
   - Кнопки "Сформировать", "Скачать архив", "Отмена"
3. Пользователь загружает файл и выбирает категорию
4. Пользователь нажимает "Сформировать"
5. Система показывает сообщение:
   ┌─────────────────────────────────────────────────────┐
   │ ⚠️ Функционал в разработке                          │
   │ Эта функция будет доступна в версии 2.0             │
   └─────────────────────────────────────────────────────┘
6. Конец
```

## 6.3. Матрица прав доступа

| Функция | Пользователь | Администратор |
|---------|--------------|---------------|
| Просмотр счетов | ✅ | ✅ |
| Создание счетов | ✅ | ✅ |
| Редактирование счетов | ✅ | ✅ |
| Удаление счетов (soft) | ✅ | ✅ |
| Формирование документов | ✅ | ✅ |
| Просмотр отчётов | ✅ | ✅ |
| Создание отчётов | ✅ | ✅ |
| Управление справочниками | ✅ | ✅ |
| Управление пользователями | ❌ | ✅ |
| Django Admin | ❌ | ✅ |
| Бэкап БД | ❌ | ✅ |

---

# 📄 07_ПРИНЦИПЫ_РАЗРАБОТКИ.md

## 7.1. Общие принципы

### 7.1.1. KISS (Keep It Simple, Stupid)
- Избегать избыточных абстракций
- Предпочитать простые решения сложным
- Один файл JS на страницу/компонент

### 7.1.2. DRY (Don't Repeat Yourself)
- Выносить повторяющуюся логику в утилиты
- Использовать базовые классы для моделей
- Общие шаблоны в `templates/components/`

### 7.1.3. Конвенция над конфигурацией
- Единый стиль именования
- Стандартная структура папок
- Шаблоны кода для типовых задач

## 7.2. Backend (Python/Django)

### 7.2.1. Function-Based Views (FBV)

```python
# ✅ ПРАВИЛЬНО: Простая FBV
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

@login_required
def bill_list(request, organization_type):
    """Список счетов для ГК или ЧОУ"""
    bills = Bill.objects.filter(
        organization_type=organization_type,
        is_archived=False
    ).select_related('contract', 'counterparty').order_by('-date')
    
    search_query = request.GET.get('q', '')
    if search_query:
        bills = bills.filter(number__icontains=search_query)
    
    return render(request, 'bills/list.html', {
        'bills': bills,
        'organization_type': organization_type,
        'search_query': search_query,
    })
```

### 7.2.2. Модели

```python
# ✅ ПРАВИЛЬНО: Наследование от BaseModel
class Bill(BaseModel):
    number = models.CharField(max_length=50)
    # ... другие поля
    
    class Meta:
        verbose_name = "Счет"
        verbose_name_plural = "Счета"
```

### 7.2.3. Формы (Django Forms)

```python
# ✅ ПРАВИЛЬНО: Явная валидация через Django Forms
# apps/bills/forms.py
from django import forms
from .models import Bill, BillItem

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['number', 'date', 'is_offer', 'contract', 'counterparty', 'power_of_attorney']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean_number(self):
        """Валидация уникальности номера счета"""
        number = self.cleaned_data.get('number')
        organization_type = self.instance.organization_type if self.instance.pk else self.initial.get('organization_type')
        
        if Bill.objects.filter(
            number=number,
            organization_type=organization_type
        ).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Счет с таким номером уже существует")
        return number
    
    def clean(self):
        """Кросс-полевая валидация"""
        cleaned_data = super().clean()
        is_offer = cleaned_data.get('is_offer')
        contract = cleaned_data.get('contract')
        counterparty = cleaned_data.get('counterparty')
        
        if is_offer and contract:
            raise forms.ValidationError("Для оферты договор указывать не нужно")
        
        if not is_offer and not contract:
            raise forms.ValidationError("Для счета по договору необходимо выбрать договор")
        
        return cleaned_data

# FormSet для позиций счета
BillItemFormSet = forms.inlineformset_factory(
    Bill,
    BillItem,
    fields=['work_type', 'description', 'unit', 'quantity', 'price'],
    extra=1,
    can_delete=True
)
```

### 7.2.4. Сервисный слой

```python
# ✅ ПРАВИЛЬНО: Вынесение бизнес-логики
# apps/bills/services/bill_generator.py

from openpyxl import load_workbook
from django.conf import settings
from pathlib import Path
from datetime import datetime

def generate_bill_excel(bill: Bill) -> tuple[Path, bool, str]:
    """
    Генерация Excel-файла для счета
    
    Returns:
        tuple: (путь_к_файлу, успех, сообщение_об_ошибке)
    """
    # Проверка обязательных полей
    if not bill.power_of_attorney:
        return None, False, "Не указана доверенность"
    
    if not bill.items.exists():
        return None, False, "Нет позиций в счете"
    
    # Выбор шаблона
    template_name = 'bill_offer_template.xlsx' if bill.is_offer else 'bill_template.xlsx'
    template_path = settings.TEMPLATES_DOC_ROOT / 'bills' / template_name
    
    # Загрузка шаблона
    wb = load_workbook(template_path)
    ws = wb.active
    
    # Заполнение данных
    ws['B2'] = bill.number
    ws['B3'] = bill.date.strftime('%d.%m.%Y')
    ws['B5'] = bill.counterparty.name if bill.counterparty else ''
    # ... остальные поля
    
    # Сохранение
    output_dir = settings.FILES_STRUCTURE['bills'] / bill.organization_type.lower()
    output_dir /= datetime.now().strftime('%Y') / datetime.now().strftime('%m')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_path = output_dir / f"Счет_{bill.number}.xlsx"
    wb.save(output_path)
    
    return output_path, True, ""
```

## 7.3. Frontend (JavaScript/HTMX/Alpine)

### 7.3.1. Vanilla JS ES2024

```javascript
// ✅ ПРАВИЛЬНО: Один файл на страницу, глобальные функции
// static/bills/js/bill_form.js

// Глобальный объект для формы счета
window.BillForm = {
    init() {
        this.bindEvents();
        this.calculateTotals();
    },
    
    bindEvents() {
        document.querySelectorAll('.bill-item-row').forEach(row => {
            row.querySelector('.quantity-input')?.addEventListener('input', (e) => {
                this.calculateRowTotal(e.target.closest('.bill-item-row'));
            });
            row.querySelector('.price-input')?.addEventListener('input', (e) => {
                this.calculateRowTotal(e.target.closest('.bill-item-row'));
            });
        });
    },
    
    calculateRowTotal(row) {
        const quantity = parseFloat(row.querySelector('.quantity-input')?.value) || 0;
        const price = parseFloat(row.querySelector('.price-input')?.value) || 0;
        const total = quantity * price;
        row.querySelector('.total-display').textContent = total.toFixed(2);
        this.calculateTotals();
    },
    
    calculateTotals() {
        let grandTotal = 0;
        document.querySelectorAll('.bill-item-row').forEach(row => {
            const rowTotal = parseFloat(row.querySelector('.total-display')?.textContent) || 0;
            grandTotal += rowTotal;
        });
        document.querySelector('.grand-total-display').textContent = grandTotal.toFixed(2);
    }
};

// Инициализация при загрузке
document.addEventListener('DOMContentLoaded', () => {
    window.BillForm.init();
});
```

### 7.3.2. HTMX Patterns

```html
<!-- ✅ ПРАВИЛЬНО: Поиск с задержкой -->
<input type="text" 
       name="q" 
       placeholder="Поиск..."
       hx-get="/api/directories/contracts/search/"
       hx-trigger="keyup changed delay:300ms"
       hx-target="#contract-results"
       hx-indicator=".htmx-indicator">

<!-- ✅ ПРАВИЛЬНО: Модальное окно -->
<div id="modal-contract" 
     class="modal" 
     hx-get="/directories/contracts/modal/"
     hx-trigger="showModal from:body"
     hx-swap="innerHTML">
</div>
```

### 7.3.3. Alpine.js Patterns

```html
<!-- ✅ ПРАВИЛЬНО: Реактивное состояние для модального окна -->
<div x-data="{ 
    modalOpen: false, 
    selectedItem: null,
    selectItem(id, name) {
        this.selectedItem = { id, name };
        this.modalOpen = false;
        document.getElementById('contract-input').value = name;
        document.getElementById('contract-id').value = id;
    }
}">
    <input type="text" id="contract-input" readonly>
    <input type="hidden" id="contract-id" name="contract">
    
    <button type="button" @click="modalOpen = true">Выбрать</button>
    
    <div x-show="modalOpen" @click.away="modalOpen = false">
        <!-- Список контрактов -->
    </div>
</div>
```

## 7.4. CSS/Bootstrap

### 7.4.1. Компоненты

```html
<!-- ✅ ПРАВИЛЬНО: Карточка с тенью -->
<div class="card shadow-sm border-0">
    <div class="card-body">
        <h5 class="card-title">Заголовок</h5>
        <p class="card-text">Содержимое</p>
    </div>
</div>
```

### 7.4.2. Отображение ошибок форм

```html
<!-- ✅ ПРАВИЛЬНО: Отображение ошибок Django Forms -->
{% if form.errors %}
<div class="alert alert-danger">
    <i class="bi bi-exclamation-circle-fill me-2"></i>
    <strong>Исправьте следующие ошибки:</strong>
    <ul class="mb-0 mt-2">
        {% for field in form %}
            {% for error in field.errors %}
            <li>{{ field.label }}: {{ error }}</li>
            {% endfor %}
        {% endfor %}
        {% for error in form.non_field_errors %}
        <li>{{ error }}</li>
        {% endfor %}
    </ul>
</div>
{% endif %}
```

## 7.5. Безопасность

### 7.5.1. Обязательные требования

```python
# settings.py

# CSRF защита
CSRF_COOKIE_SECURE = True  # Для HTTPS
CSRF_COOKIE_HTTPONLY = True

# Session защита
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Авторизация
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
```

### 7.5.2. Декораторы views

```python
from django.contrib.auth.decorators import login_required

@login_required
def my_view(request):
    # Все views защищены
    pass
```

### 7.5.3. Переменные окружения

- Все секреты только через `.env`
- `.env.example` с заглушками в репозитории
- Никогда не коммитить `.env` в git

## 7.6. Логирование

```python
# settings.py

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'D:/DnIT_Files/logs/app.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'apps': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

---

# 📄 08_UI_UX_РЕКОМЕНДАЦИИ.md

## 8.1. Навигация и меню

### 8.1.1. Структура главной страницы

```
┌─────────────────────────────────────────────────────────────────┐
│  🏠 ДНиТ. Управление. Астрахань              👤 User | 🚪 Выход │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │                 │  │                 │  │                 │  │
│  │      🏢 ГК      │  │      🎓 ЧОУ     │  │      📚         │  │
│  │   (Группа       │  │   (Частное      │  │   СПРАВОЧНИКИ   │  │
│  │    компаний)    │  │    образов.     │  │                 │  │
│  │                 │  │    учреждение)   │  │                 │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  📋 Справочники (быстрый доступ)                            ││
│  │  [Виды работ] [Ед.изм.] [Договоры] [Контрагенты]            ││
│  │  [Доверенности] [Ответственные лица]                        ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  ⚠️ ПРОТОКОЛЫ И УДОСТОВЕРЕНИЯ (в разработке)                ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 8.2. Реестр счетов (Таблица)

### 8.2.1. Рекомендации для таблиц с большим количеством колонок

```html
<!-- ✅ ПРАВИЛЬНО: Таблица с горизонтальной прокруткой и фиксированными колонками -->
<div class="table-container" style="overflow-x: auto;">
    <table class="table table-hover table-bordered table-full-width">
        <thead class="table-light sticky-top">
            <tr>
                <th style="min-width: 50px;" class="text-center">
                    <input type="checkbox" class="form-check-input" id="select-all">
                </th>
                <th style="min-width: 100px;">№ Счета</th>
                <th style="min-width: 100px;">Дата</th>
                <th style="min-width: 80px;">Тип</th>
                <th style="min-width: 200px;">Договор</th>
                <th style="min-width: 250px;">Контрагент</th>
                <th style="min-width: 100px;">Сумма</th>
                <th style="min-width: 100px;">Статус</th>
                <th style="min-width: 150px;" class="text-end">Действия</th>
            </tr>
        </thead>
        <tbody>
            {% for bill in bills %}
            <tr class="{% if bill.is_archived %}table-secondary{% endif %}">
                <td class="text-center">
                    <input type="checkbox" class="form-check-input bill-checkbox" value="{{ bill.id }}">
                </td>
                <td class="fw-bold">{{ bill.number }}</td>
                <td>{{ bill.date|date:"d.m.Y" }}</td>
                <td>
                    {% if bill.is_offer %}
                        <span class="badge bg-info">Оферта</span>
                    {% else %}
                        <span class="badge bg-secondary">Договор</span>
                    {% endif %}
                </td>
                <td>{{ bill.contract|default:"—" }}</td>
                <td title="{{ bill.counterparty.name }}">{{ bill.counterparty.name|truncatechars:50|default:"—" }}</td>
                <td class="text-end">{{ bill.total_amount|floatformat:2 }} ₽</td>
                <td>
                    {% if bill.status == 'GENERATED' %}
                        <span class="badge bg-success">Сформирован</span>
                    {% else %}
                        <span class="badge bg-warning">Черновик</span>
                    {% endif %}
                </td>
                <td class="text-end">
                    <a href="{% url 'bills:detail' bill.pk %}" class="btn btn-sm btn-outline-primary">👁️</a>
                    <a href="{% url 'bills:edit' bill.pk %}" class="btn btn-sm btn-outline-secondary">✏️</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>
```

## 8.3. Форма создания/редактирования счета

### 8.3.1. Layout формы

```
┌─────────────────────────────────────────────────────────────────┐
│  📝 Счет № _______                          [Сохранить] [Сформировать] │
├─────────────────────────────────────────────────────────────────┤
│  {% if form.errors %}                                           │
│  <div class="alert alert-danger">{{ form.errors }}</div>        │
│  {% endif %}                                                    │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 📋 Основная информация                                      ││
│  │ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            ││
│  │ │ № Счета     │ │ Дата        │ │ ☐ Оферта    │            ││
│  │ │ [12-1/А   ] │ │ [13.03.2026]│ │             │            ││
│  │ └─────────────┘ └─────────────┘ └─────────────┘            ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │ 📦 Позиции счета (FormSet)               [+ Добавить строку]││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                 │
│  [Сохранить]  [Сформировать]  [🔴 X Сбросить статус]  [Отмена] │
└─────────────────────────────────────────────────────────────────┘
```

### 8.3.2. Блокировка полей при статусе "Сформирован"

```html
{% if bill.status == 'GENERATED' %}
    <div class="alert alert-warning d-flex align-items-center">
        <i class="bi bi-lock-fill me-2"></i>
        <div>
            <strong>Счет сформирован.</strong> 
            Поля заблокированы для редактирования.
            {% if bill.can_reset_status %}
                Нажмите 🔴 для сброса статуса.
            {% else %}
                Сначала исключите счет из отчётов.
            {% endif %}
        </div>
    </div>
    
    <script>
        document.querySelectorAll('input, select, textarea').forEach(el => {
            el.disabled = true;
        });
    </script>
{% endif %}
```

## 8.4. Модальные окна

### 8.4.1. Выбор сущности

```html
<div class="modal fade" id="selectModal" tabindex="-1">
    <div class="modal-dialog modal-lg">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">📋 Выбор {{ entity_name }}</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                <input type="text" 
                       class="form-control" 
                       placeholder="Поиск..."
                       hx-get="{{ search_url }}"
                       hx-trigger="keyup changed delay:300ms"
                       hx-target="#select-results">
                <div id="select-results" hx-get="{{ list_url }}" hx-trigger="load"></div>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Отмена</button>
                <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#createModal">
                    ➕ Добавить новую
                </button>
            </div>
        </div>
    </div>
</div>
```

## 8.5. Уведомления (Toasts)

```html
<div class="toast-container position-fixed bottom-0 end-0 p-3">
    <div id="liveToast" class="toast" role="alert">
        <div class="toast-header">
            <i class="bi bi-check-circle-fill text-success me-2"></i>
            <strong class="me-auto">Успешно</strong>
            <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
        </div>
        <div class="toast-body">{{ message }}</div>
    </div>
</div>
```

## 8.6. Цветовая схема

| Элемент | Цвет | Bootstrap Class |
|---------|------|-----------------|
| ГК | Синий | `bg-primary` |
| ЧОУ | Зелёный | `bg-success` |
| Справочники | Фиолетовый | `bg-purple` |
| Черновик | Жёлтый | `badge bg-warning` |
| Сформирован | Зелёный | `badge bg-success` |
| Оферта | Голубой | `badge bg-info` |
| Договор | Серый | `badge bg-secondary` |
| Опасное действие | Красный | `btn-danger` |

---

# 📄 09_ПЛАН_РАЗРАБОТКИ.md

## 9.1. Этапы разработки (Roadmap)

```
┌─────────────────────────────────────────────────────────────────┐
│ ЭТАП 1: ПОДГОТОВКА (Неделя 1)                                   │
├─────────────────────────────────────────────────────────────────┤
│ □ Настройка окружения разработки                                │
│ □ Инициализация Django проекта                                  │
│ □ Настройка PostgreSQL                                          │
│ □ Создание .env и .env.example                                  │
│ □ Настройка python-decouple                                     │
│ □ Настройка Bootstrap + HTMX + Alpine.js                        │
│ □ Создание базовых шаблонов (base.html, navbar)                 │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ ЭТАП 2: СПРАВОЧНИКИ (Неделя 2)                                  │
├─────────────────────────────────────────────────────────────────┤
│ □ Модели справочников (WorkType, Unit, Counterparty...)         │
│ □ Django Forms для справочников                                 │
│ □ CRUD views для справочников                                   │
│ □ Модальные окна выбора                                         │
│ □ Тестирование справочников                                     │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ ЭТАП 3: СЧЕТА (Недели 3-4)                                      │
├─────────────────────────────────────────────────────────────────┤
│ □ Модели Bill, BillItem                                         │
│ □ Django Forms (BillForm, BillItemFormSet)                      │
│ □ Форма создания/редактирования счета                           │
│ □ Логика оферта/договор                                         │
│ □ Динамические строки позиций                                   │
│ □ Статусы и блокировка                                          │
│ □ Реестр счетов с фильтрацией                                   │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ ЭТАП 4: ОТЧЁТЫ (Недели 5-6)                                     │
├─────────────────────────────────────────────────────────────────┤
│ □ Модели отчётов (Daily, Weekly, IN, AVR)                       │
│ □ Django Forms для отчётов                                      │
│ □ CRUD views для отчётов                                        │
│ □ Выбор счетов для отчёта                                       │
│ □ Связи счет ↔ отчёт                                            │
│ □ Каскадное удаление связей                                     │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ ЭТАП 5: ГЕНЕРАЦИЯ ДОКУМЕНТОВ (Недели 7-8)                       │
├─────────────────────────────────────────────────────────────────┤
│ □ Интеграция openpyxl для Excel                                 │
│ □ Интеграция docxtpl для Word                                   │
│ □ Шаблоны документов (предоставленные)                          │
│ □ Пакетное формирование счетов                                  │
│ □ Логирование ошибок генерации                                  │
│ □ Экспорт реестров в Excel                                      │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ ЭТАП 6: ПРОТОКОЛЫ (Неделя 9)                                    │
├─────────────────────────────────────────────────────────────────┤
│ □ Заглушка функционала                                          │
│ □ UI формы (без backend-логики)                                 │
│ □ Сообщение "В разработке"                                      │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ ЭТАП 7: ДЕПЛОЙ (Неделя 10)                                      │
├─────────────────────────────────────────────────────────────────┤
│ □ Настройка Waitress + SSL                                      │
│ □ Настройка NSSM для автозапуска                                │
│ □ Скрипт бэкапа БД + Task Scheduler                             │
│ □ Тестирование во внутренней сети                               │
│ □ Обучение пользователей                                        │
└─────────────────────────────────────────────────────────────────┘
```

## 9.2. Детальный план по спринтам

### Спринт 1 (Неделя 1-2): Foundation

| Задача | Оценка (ч) | Статус |
|--------|------------|--------|
| Инициализация Django проекта | 2 | □ |
| Настройка PostgreSQL | 2 | □ |
| Создание .env и .env.example | 1 | □ |
| Настройка python-decouple | 1 | □ |
| Настройка Bootstrap 5 + HTMX + Alpine.js | 4 | □ |
| Создание base.html и компонентов | 4 | □ |
| Модели справочников | 4 | □ |
| Django Forms для справочников | 4 | □ |
| CRUD для справочников | 8 | □ |
| **Итого** | **30 ч** | |

### Спринт 2 (Неделя 3-4): Bills Core

| Задача | Оценка (ч) | Статус |
|--------|------------|--------|
| Модели Bill, BillItem | 4 | □ |
| Django Forms (BillForm, FormSet) | 6 | □ |
| Форма создания счета | 8 | □ |
| Динамические строки позиций | 6 | □ |
| Логика оферта/договор/контрагент | 6 | □ |
| Реестр счетов + поиск | 6 | □ |
| Статусы и блокировка | 4 | □ |
| **Итого** | **40 ч** | |

### Спринт 3 (Неделя 5-6): Reports

| Задача | Оценка (ч) | Статус |
|--------|------------|--------|
| Модели отчётов (4 типа) | 4 | □ |
| Django Forms для отчётов | 4 | □ |
| CRUD для отчётов | 8 | □ |
| Выбор счетов для отчёта | 6 | □ |
| Связи и каскадное удаление | 6 | □ |
| Реестры отчётов | 4 | □ |
| **Итого** | **32 ч** | |

### Спринт 4 (Неделя 7-8): Document Generation

| Задача | Оценка (ч) | Статус |
|--------|------------|--------|
| openpyxl интеграция | 6 | □ |
| docxtpl интеграция | 6 | □ |
| Шаблоны счетов (2 шт) | 4 | □ |
| Шаблоны отчётов (4 шт) | 8 | □ |
| Пакетное формирование | 8 | □ |
| Логирование ошибок | 4 | □ |
| Экспорт в Excel | 4 | □ |
| **Итого** | **40 ч** | |

### Спринт 5 (Неделя 9-10): Deployment

| Задача | Оценка (ч) | Статус |
|--------|------------|--------|
| Waitress + SSL настройка | 4 | □ |
| NSSM автозапуск | 2 | □ |
| Скрипт бэкапа БД | 4 | □ |
| Task Scheduler настройка | 2 | □ |
| Тестирование | 8 | □ |
| Документация | 4 | □ |
| **Итого** | **24 ч** | |

**Общая оценка: 166 часов (~4 недели full-time)**

## 9.3. Критерии готовности (Definition of Done)

### Для каждой задачи:
- [ ] Код написан и закоммичен
- [ ] Код протестирован вручную
- [ ] Нет console errors в браузере
- [ ] Работает на Chrome и Firefox
- [ ] Документация обновлена

### Для MVP (Этапы 1-4):
- [ ] Все справочники работают (CRUD + Forms)
- [ ] Счета создаются/редактируются/удаляются
- [ ] Валидация Django Forms работает
- [ ] Статусы счетов работают
- [ ] Отчёты создаются и связываются со счетами
- [ ] Блокировка счёта при наличии связей работает

### Для Production (Все этапы):
- [ ] Генерация документов работает
- [ ] Пакетное формирование работает
- [ ] .env настроен правильно
- [ ] Бэкап БД настроен
- [ ] SSL настроен
- [ ] Автозапуск через NSSM работает

---

# 📄 10_ЧЕК_ЛИСТ_ГОТОВНОСТИ.md

## 10.1. Pre-Development Checklist

### Окружение разработки
- [ ] Python 3.13+ установлен
- [ ] PostgreSQL 15+ установлен и настроен
- [ ] VSCode с расширениями (Python, Django, PostgreSQL)
- [ ] Git настроен
- [ ] Virtual environment создан
- [ ] requirements.txt заполнен

### Проект
- [ ] Django проект инициализирован
- [ ] Приложения созданы (core, accounts, bills, reports, directories, protocols)
- [ ] settings.py настроен (DATABASES, STATIC, MEDIA, FILES)
- [ ] **.env создан с SECRET_KEY**
- [ ] **.env.example создан для команды**
- [ ] **.env добавлен в .gitignore**
- [ ] **python-decouple настроен**
- [ ] .gitignore настроен

## 10.2. Development Checklist

### Справочники (Directories)
- [ ] Модели созданы и мигрированы
- [ ] **Django Forms созданы для всех моделей**
- [ ] CRUD views работают
- [ ] **Валидация форм работает**
- [ ] **Ошибки отображаются в UI**
- [ ] Модальные окна выбора работают
- [ ] Soft delete работает
- [ ] Поиск/фильтрация работает

### Счета (Bills)
- [ ] Модели Bill, BillItem созданы
- [ ] **BillForm и BillItemFormSet созданы**
- [ ] **Кастомная валидация полей (clean_number, clean)**
- [ ] Форма создания/редактирования работает
- [ ] Динамические строки позиций работают
- [ ] Логика оферта/договор работает
- [ ] Статусы (DRAFT/GENERATED) работают
- [ ] Блокировка при наличии связей работает
- [ ] Реестр с поиском работает
- [ ] Пакетное формирование работает

### Отчёты (Reports)
- [ ] 4 модели отчётов созданы
- [ ] **Django Forms для отчётов созданы**
- [ ] CRUD views работают
- [ ] Выбор счетов для отчёта работает
- [ ] Связи обновляются корректно
- [ ] Каскадное удаление связей работает

### Генерация документов
- [ ] openpyxl генерирует Excel
- [ ] docxtpl генерирует Word
- [ ] Шаблоны заполняются корректно
- [ ] Файлы сохраняются в правильную структуру
- [ ] Скачивание работает
- [ ] Ошибки логируются

### Frontend
- [ ] Bootstrap 5 подключён
- [ ] HTMX работает (поиск, модальные окна)
- [ ] Alpine.js работает (реактивность)
- [ ] Vanilla JS ES2024 (без import/export)
- [ ] Адаптивность проверена
- [ ] Нет console errors

### Безопасность
- [ ] @login_required на всех views
- [ ] CSRF токены работают
- [ ] XSS защита включена
- [ ] SQL injection защищено (ORM)
- [ ] **SECRET_KEY не в коде**
- [ ] **.env не в git**

## 10.3. Pre-Deployment Checklist

### Сервер
- [ ] Windows 10/11 настроен
- [ ] PostgreSQL установлен на сервере
- [ ] Python 3.13+ установлен
- [ ] **Переменные окружения настроены (.env на сервере)**
- [ ] Папка D:/DnIT_Files/ создана
- [ ] Структура папок создана

### Приложение
- [ ] collectstatic выполнен
- [ ] Миграции применены
- [ ] Суперпользователь создан
- [ ] Шаблоны документов скопированы
- [ ] settings.py для production настроен

### Waitress + SSL
- [ ] Waitress установлен
- [ ] Самоподписанный SSL сертификат создан
- [ ] Waitress настроен на HTTPS
- [ ] Порт открыт во внутренней сети

### NSSM
- [ ] NSSM установлен
- [ ] Служба создана
- [ ] Автозапуск проверен
- [ ] Логи службы настроены

### Бэкап
- [ ] Скрипт backup_db.py написан
- [ ] Task Scheduler настроен (ежедневно)
- [ ] Тестовый бэкап выполнен
- [ ] Восстановление из бэкапа протестировано

## 10.4. Post-Deployment Checklist

### Тестирование
- [ ] Авторизация работает
- [ ] Все справочники работают
- [ ] Создание счета работает
- [ ] **Валидация форм работает**
- [ ] Формирование счета работает
- [ ] Создание отчёта работает
- [ ] Пакетное формирование работает
- [ ] Экспорт в Excel работает
- [ ] Soft delete работает
- [ ] Бэкап выполняется по расписанию

### Документация
- [ ] README.md обновлён
- [ ] Инструкция для пользователей написана
- [ ] Контакты поддержки указаны

### Обучение
- [ ] Пользователи обучены
- [ ] Обратная связь получена
- [ ] Баг-лист составлен

## 10.5. Maintenance Checklist

### Ежедневно
- [ ] Проверка логов приложения
- [ ] Проверка выполнения бэкапа

### Еженедельно
- [ ] Проверка свободного места на диске
- [ ] Проверка логов ошибок

### Ежемесячно
- [ ] Обновление зависимостей (security patches)
- [ ] Архивация старых бэкапов
- [ ] Проверка SSL сертификата

---
