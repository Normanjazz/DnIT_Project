from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import WorkType, Unit, Counterparty, Contract, ResponsiblePerson, PowerOfAttorney
from .forms import WorkTypeForm, UnitForm, CounterpartyForm, ContractForm, ResponsiblePersonForm, PowerOfAttorneyForm


# =============================================================================
# WorkType (Виды работ) - CRUD Views
# =============================================================================

@login_required
def work_type_list(request):
    """
    Список видов работ с поиском и фильтрацией.
    """
    # Получаем все неархивированные виды работ
    work_types = WorkType.objects.all().order_by('full_name')
    
    # Поиск по полному или сокращённому наименованию
    
    search_query = request.GET.get('q', '') # Получает параметр поиска из URL (например, ?q=монтаж)
    if search_query:
        work_types = work_types.filter(
            Q(full_name__icontains=search_query) |
            Q(short_name__icontains=search_query) # Q(field__icontains=value) - Регистронезависимый поиск по полю (монтаж = МОНТАЖ = Монтаж)
        )
    
    context = {
        'work_types': work_types,
        'search_query': search_query,
        'page_title': 'Виды работ',
    }
    
    return render(request, 'directories/work_type_list.html', context)


@login_required
def work_type_create(request):
    """
    Создание нового вида работ.
    """
    form = WorkTypeForm(request.POST or None) # Передаёт данные формы при POST-запросе, иначе None (для создания пустой формы)
    
    if request.method == 'POST':
        if form.is_valid():
            # Сохраняем объект, но не коммитим в БД сразу
            work_type = form.save(commit=False)
            work_type.created_by = request.user  # Запоминаем кто создал
            work_type.save()
            
            # Сообщение об успехе
            messages.success(request, f'Вид работ "{work_type.full_name}" успешно создан!')
            
            # Перенаправляем на список
            return redirect('directories:work_type_list')
    
    context = {
        'form': form,
        'page_title': 'Создать вид работ',
        'action': 'create',
    }
    
    return render(request, 'directories/work_type_form.html', context)


@login_required
def work_type_detail(request, pk):
    """
    Просмотр деталей вида работ.
    """
    work_type = get_object_or_404(WorkType, pk=pk)
    
    context = {
        'work_type': work_type,
        'page_title': 'Просмотр вида работ',
    }
    
    return render(request, 'directories/work_type_detail.html', context)


@login_required
def work_type_update(request, pk):
    """
    Редактирование вида работ.
    """
    # Получаем объект или 404
    work_type = get_object_or_404(WorkType, pk=pk)
    
    form = WorkTypeForm(request.POST or None, instance=work_type)
    
    if request.method == 'POST':
        if form.is_valid():
            work_type = form.save(commit=False)
            work_type.created_by = request.user  # Обновляем кто изменил
            work_type.save()
            
            messages.success(request, f'Вид работ "{work_type.full_name}" успешно обновлён!')
            return redirect('directories:work_type_list')
    
    context = {
        'form': form,
        'work_type': work_type,
        'page_title': 'Редактировать вид работ',
        'action': 'update',
    }
    
    return render(request, 'directories/work_type_form.html', context)


@login_required
def work_type_delete(request, pk):
    """
    Мягкое удаление вида работ (soft delete).
    """
    work_type = get_object_or_404(WorkType, pk=pk)
    
    if request.method == 'POST':
        work_type.archive()  # Мягкое удаление через метод модели
        
        messages.success(request, f'Вид работ "{work_type.full_name}" успешно удалён!')
        return redirect('directories:work_type_list')
    
    context = {
        'work_type': work_type,
        'page_title': 'Удалить вид работ',
    }
    
    return render(request, 'directories/work_type_confirm_delete.html', context)

# =============================================================================
# Unit (Единицы измерения) - CRUD Views
# =============================================================================

@login_required
def unit_list(request):
    """
    Список единиц измерения с поиском и фильтрацией.
    """
    # Получаем все неархивированные единицы измерения
    units = Unit.objects.all().order_by('full_name')
    
    # Поиск по полному или сокращённому наименованию
    search_query = request.GET.get('q', '')
    if search_query:
        units = units.filter(
            Q(full_name__icontains=search_query) |
            Q(short_name__icontains=search_query)
        )
    
    context = {
        'units': units,
        'search_query': search_query,
        'page_title': 'Единицы измерения',
    }
    
    return render(request, 'directories/unit_list.html', context)


@login_required
def unit_create(request):
    """
    Создание новой единицы измерения.
    """
    form = UnitForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            # Сохраняем объект, но не коммитим в БД сразу
            unit = form.save(commit=False)
            unit.created_by = request.user  # Запоминаем кто создал
            unit.save()
            
            # Сообщение об успехе
            messages.success(request, f'Единица измерения "{unit.full_name}" успешно создана!')
            
            # Перенаправляем на список
            return redirect('directories:unit_list')
    
    context = {
        'form': form,
        'page_title': 'Создать единицу измерения',
        'action': 'create',
    }
    
    return render(request, 'directories/unit_form.html', context)


@login_required
def unit_detail(request, pk):
    """
    Просмотр деталей единицы измерения.
    """
    unit = get_object_or_404(Unit, pk=pk)
    
    context = {
        'unit': unit,
        'page_title': 'Просмотр единицы измерения',
    }
    
    return render(request, 'directories/unit_detail.html', context)


@login_required
def unit_update(request, pk):
    """
    Редактирование единицы измерения.
    """
    # Получаем объект или 404
    unit = get_object_or_404(Unit, pk=pk)
    
    form = UnitForm(request.POST or None, instance=unit)
    
    if request.method == 'POST':
        if form.is_valid():
            unit = form.save(commit=False)
            unit.created_by = request.user  # Обновляем кто изменил
            unit.save()
            
            messages.success(request, f'Единица измерения "{unit.full_name}" успешно обновлена!')
            return redirect('directories:unit_list')
    
    context = {
        'form': form,
        'unit': unit,
        'page_title': 'Редактировать единицу измерения',
        'action': 'update',
    }
    
    return render(request, 'directories/unit_form.html', context)


@login_required
def unit_delete(request, pk):
    """
    Мягкое удаление единицы измерения (soft delete).
    """
    unit = get_object_or_404(Unit, pk=pk)
    
    if request.method == 'POST':
        unit.archive()  # Мягкое удаление через метод модели
        
        messages.success(request, f'Единица измерения "{unit.full_name}" успешно удалена!')
        return redirect('directories:unit_list')
    
    context = {
        'unit': unit,
        'page_title': 'Удалить единицу измерения',
    }
    
    return render(request, 'directories/unit_confirm_delete.html', context)


# =============================================================================
# Counterparty (Контрагенты) - STUB Views
# =============================================================================

@login_required
def counterparty_list(request):
    """Заглушка: Список контрагентов"""
    return render(request, 'directories/counterparty_list.html', {'page_title': 'Контрагенты'})

@login_required
def counterparty_create(request):
    """Заглушка: Создание контрагента"""
    return render(request, 'directories/counterparty_form.html', {'page_title': 'Создать контрагента'})

@login_required
def counterparty_detail(request, pk):
    """Заглушка: Просмотр контрагента"""
    return render(request, 'directories/counterparty_detail.html', {'page_title': 'Контрагент'})

@login_required
def counterparty_update(request, pk):
    """Заглушка: Редактирование контрагента"""
    return render(request, 'directories/counterparty_form.html', {'page_title': 'Редактировать контрагента'})

@login_required
def counterparty_delete(request, pk):
    """Заглушка: Удаление контрагента"""
    return render(request, 'directories/counterparty_confirm_delete.html', {'page_title': 'Удалить контрагента'})


# =============================================================================
# Contract (Договоры) - STUB Views
# =============================================================================

@login_required
def contract_list(request):
    """Заглушка: Список договоров"""
    return render(request, 'directories/contract_list.html', {'page_title': 'Договоры'})

@login_required
def contract_create(request):
    """Заглушка: Создание договора"""
    return render(request, 'directories/contract_form.html', {'page_title': 'Создать договор'})

@login_required
def contract_detail(request, pk):
    """Заглушка: Просмотр договора"""
    return render(request, 'directories/contract_detail.html', {'page_title': 'Договор'})

@login_required
def contract_update(request, pk):
    """Заглушка: Редактирование договора"""
    return render(request, 'directories/contract_form.html', {'page_title': 'Редактировать договор'})

@login_required
def contract_delete(request, pk):
    """Заглушка: Удаление договора"""
    return render(request, 'directories/contract_confirm_delete.html', {'page_title': 'Удалить договор'})


# =============================================================================
# ResponsiblePerson (Ответственные лица) - STUB Views
# =============================================================================

@login_required
def responsible_person_list(request):
    """Заглушка: Список ответственных лиц"""
    return render(request, 'directories/responsible_person_list.html', {'page_title': 'Ответственные лица'})

@login_required
def responsible_person_create(request):
    """Заглушка: Создание ответственного лица"""
    return render(request, 'directories/responsible_person_form.html', {'page_title': 'Создать ответственное лицо'})

@login_required
def responsible_person_detail(request, pk):
    """Заглушка: Просмотр ответственного лица"""
    return render(request, 'directories/responsible_person_detail.html', {'page_title': 'Ответственное лицо'})

@login_required
def responsible_person_update(request, pk):
    """Заглушка: Редактирование ответственного лица"""
    return render(request, 'directories/responsible_person_form.html', {'page_title': 'Редактировать ответственное лицо'})

@login_required
def responsible_person_delete(request, pk):
    """Заглушка: Удаление ответственного лица"""
    return render(request, 'directories/responsible_person_confirm_delete.html', {'page_title': 'Удалить ответственное лицо'})


# =============================================================================
# PowerOfAttorney (Доверенности) - STUB Views
# =============================================================================

@login_required
def power_of_attorney_list(request):
    """Заглушка: Список доверенностей"""
    return render(request, 'directories/power_of_attorney_list.html', {'page_title': 'Доверенности'})

@login_required
def power_of_attorney_create(request):
    """Заглушка: Создание доверенности"""
    return render(request, 'directories/power_of_attorney_form.html', {'page_title': 'Создать доверенность'})

@login_required
def power_of_attorney_detail(request, pk):
    """Заглушка: Просмотр доверенности"""
    return render(request, 'directories/power_of_attorney_detail.html', {'page_title': 'Доверенность'})

@login_required
def power_of_attorney_update(request, pk):
    """Заглушка: Редактирование доверенности"""
    return render(request, 'directories/power_of_attorney_form.html', {'page_title': 'Редактировать доверенность'})

@login_required
def power_of_attorney_delete(request, pk):
    """Заглушка: Удаление доверенности"""
    return render(request, 'directories/power_of_attorney_confirm_delete.html', {'page_title': 'Удалить доверенность'})


# =============================================================================
# HTMX Partials (для модальных окон) - STUB Views
# =============================================================================

@login_required
def htmx_contract_search(request):
    """Заглушка: HTMX поиск договоров"""
    return render(request, 'directories/partials/contract_search_results.html', {})

@login_required
def htmx_counterparty_search(request):
    """Заглушка: HTMX поиск контрагентов"""
    return render(request, 'directories/partials/counterparty_search_results.html', {})

@login_required
def htmx_responsible_person_search(request):
    """Заглушка: HTMX поиск ответственных лиц"""
    return render(request, 'directories/partials/responsible_person_search_results.html', {})