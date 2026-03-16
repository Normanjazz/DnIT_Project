
from django.urls import path
from . import views

app_name = 'directories' # Пространство имён для URL (позволяет использовать {% url 'directories:work_type_list' %})

urlpatterns = [
    # ─────────────────────────────────────────────────────────────
    # WorkType (Виды работ)
    # ─────────────────────────────────────────────────────────────
    path('work-types/', views.work_type_list, name='work_type_list'),
    path('work-types/create/', views.work_type_create, name='work_type_create'),
    path('work-types/<int:pk>/', views.work_type_detail, name='work_type_detail'),
    path('work-types/<int:pk>/update/', views.work_type_update, name='work_type_update'),
    path('work-types/<int:pk>/delete/', views.work_type_delete, name='work_type_delete'),
    
    # ─────────────────────────────────────────────────────────────
    # Unit (Единицы измерения)
    # ─────────────────────────────────────────────────────────────
    path('units/', views.unit_list, name='unit_list'),
    path('units/create/', views.unit_create, name='unit_create'),
    path('units/<int:pk>/', views.unit_detail, name='unit_detail'),
    path('units/<int:pk>/update/', views.unit_update, name='unit_update'),
    path('units/<int:pk>/delete/', views.unit_delete, name='unit_delete'),
    
    # ─────────────────────────────────────────────────────────────
    # Counterparty (Контрагенты)
    # ─────────────────────────────────────────────────────────────
    path('counterparties/', views.counterparty_list, name='counterparty_list'),
    path('counterparties/create/', views.counterparty_create, name='counterparty_create'),
    path('counterparties/<int:pk>/', views.counterparty_detail, name='counterparty_detail'),
    path('counterparties/<int:pk>/update/', views.counterparty_update, name='counterparty_update'),
    path('counterparties/<int:pk>/delete/', views.counterparty_delete, name='counterparty_delete'),
    
    # ─────────────────────────────────────────────────────────────
    # Contract (Договоры)
    # ─────────────────────────────────────────────────────────────
    path('contracts/', views.contract_list, name='contract_list'),
    path('contracts/create/', views.contract_create, name='contract_create'),
    path('contracts/<int:pk>/', views.contract_detail, name='contract_detail'),
    path('contracts/<int:pk>/update/', views.contract_update, name='contract_update'),
    path('contracts/<int:pk>/delete/', views.contract_delete, name='contract_delete'),
    
    # ─────────────────────────────────────────────────────────────
    # ResponsiblePerson (Ответственные лица)
    # ─────────────────────────────────────────────────────────────
    path('responsible-persons/', views.responsible_person_list, name='responsible_person_list'),
    path('responsible-persons/create/', views.responsible_person_create, name='responsible_person_create'),
    path('responsible-persons/<int:pk>/', views.responsible_person_detail, name='responsible_person_detail'),
    path('responsible-persons/<int:pk>/update/', views.responsible_person_update, name='responsible_person_update'),
    path('responsible-persons/<int:pk>/delete/', views.responsible_person_delete, name='responsible_person_delete'),
    
    # ─────────────────────────────────────────────────────────────
    # PowerOfAttorney (Доверенности)
    # ─────────────────────────────────────────────────────────────
    path('powers-of-attorney/', views.power_of_attorney_list, name='power_of_attorney_list'),
    path('powers-of-attorney/create/', views.power_of_attorney_create, name='power_of_attorney_create'),
    path('powers-of-attorney/<int:pk>/', views.power_of_attorney_detail, name='power_of_attorney_detail'),
    path('powers-of-attorney/<int:pk>/update/', views.power_of_attorney_update, name='power_of_attorney_update'),
    path('powers-of-attorney/<int:pk>/delete/', views.power_of_attorney_delete, name='power_of_attorney_delete'),
    
    # ─────────────────────────────────────────────────────────────
    # HTMX Partials (для модальных окон выбора)
    # ─────────────────────────────────────────────────────────────
    path('htmx/contracts/search/', views.htmx_contract_search, name='htmx_contract_search'),
    path('htmx/counterparties/search/', views.htmx_counterparty_search, name='htmx_counterparty_search'),
    path('htmx/responsible-persons/search/', views.htmx_responsible_person_search, name='htmx_responsible_person_search'),
    path('htmx/powers-of-attorney/search/', views.htmx_power_of_attorney_search, name='htmx_power_of_attorney_search'),
    path('htmx/work-types/search/', views.htmx_work_type_search, name='htmx_work_type_search'),
    path('htmx/units/search/', views.htmx_unit_search, name='htmx_unit_search'),
    # ─────────────────────────────────────────────────────────────
]