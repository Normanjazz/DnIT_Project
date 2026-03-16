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
# Counterparty (Контрагенты) - CRUD Views
# =============================================================================

@login_required
def counterparty_list(request):
    """
    Список контрагентов с поиском и фильтрацией.
    """
    # Получаем все неархивированные контрагенты
    counterparties = Counterparty.objects.all().order_by('name')
    
    # Поиск по наименованию, ИНН или email
    search_query = request.GET.get('q', '')
    if search_query:
        counterparties = counterparties.filter(
            Q(name__icontains=search_query) |
            Q(inn__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    context = {
        'counterparties': counterparties,
        'search_query': search_query,
        'page_title': 'Контрагенты',
    }
    
    return render(request, 'directories/counterparty_list.html', context)


@login_required
def counterparty_create(request):
    """
    Создание нового контрагента.
    """
    form = CounterpartyForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            # Сохраняем объект, но не коммитим в БД сразу
            counterparty = form.save(commit=False)
            counterparty.created_by = request.user  # Запоминаем кто создал
            counterparty.save()
            
            # Сообщение об успехе
            messages.success(request, f'Контрагент "{counterparty.name}" успешно создан!')
            
            # Перенаправляем на список
            return redirect('directories:counterparty_list')
    
    context = {
        'form': form,
        'page_title': 'Создать контрагента',
        'action': 'create',
    }
    
    return render(request, 'directories/counterparty_form.html', context)


@login_required
def counterparty_detail(request, pk):
    """
    Просмотр деталей контрагента.
    """
    counterparty = get_object_or_404(Counterparty, pk=pk)
    
    context = {
        'counterparty': counterparty,
        'page_title': 'Просмотр контрагента',
    }
    
    return render(request, 'directories/counterparty_detail.html', context)


@login_required
def counterparty_update(request, pk):
    """
    Редактирование контрагента.
    """
    # Получаем объект или 404
    counterparty = get_object_or_404(Counterparty, pk=pk)
    
    form = CounterpartyForm(request.POST or None, instance=counterparty)
    
    if request.method == 'POST':
        if form.is_valid():
            counterparty = form.save(commit=False)
            counterparty.created_by = request.user  # Обновляем кто изменил
            counterparty.save()
            
            messages.success(request, f'Контрагент "{counterparty.name}" успешно обновлён!')
            return redirect('directories:counterparty_list')
    
    context = {
        'form': form,
        'counterparty': counterparty,
        'page_title': 'Редактировать контрагента',
        'action': 'update',
    }
    
    return render(request, 'directories/counterparty_form.html', context)


@login_required
def counterparty_delete(request, pk):
    """
    Мягкое удаление контрагента (soft delete).
    """
    counterparty = get_object_or_404(Counterparty, pk=pk)
    
    if request.method == 'POST':
        counterparty.archive()  # Мягкое удаление через метод модели
        
        messages.success(request, f'Контрагент "{counterparty.name}" успешно удалён!')
        return redirect('directories:counterparty_list')
    
    context = {
        'counterparty': counterparty,
        'page_title': 'Удалить контрагента',
    }
    
    return render(request, 'directories/counterparty_confirm_delete.html', context)


# =============================================================================
# Contract (Договоры) - CRUD Views
# =============================================================================

@login_required
def contract_list(request):
    """
    Список договоров с поиском и фильтрацией.
    """
    # Получаем все неархивированные договоры с связанными контрагентами
    contracts = Contract.objects.select_related('counterparty').all().order_by('-date', 'number')
    
    # Поиск по номеру или наименованию контрагента
    search_query = request.GET.get('q', '')
    if search_query:
        contracts = contracts.filter(
            Q(number__icontains=search_query) |
            Q(counterparty__name__icontains=search_query)
        )
    
    context = {
        'contracts': contracts,
        'search_query': search_query,
        'page_title': 'Договоры',
    }
    
    return render(request, 'directories/contract_list.html', context)


@login_required
def contract_create(request):
    """
    Создание нового договора.
    """
    form = ContractForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            # Сохраняем объект, но не коммитим в БД сразу
            contract = form.save(commit=False)
            contract.created_by = request.user  # Запоминаем кто создал
            contract.save()
            
            # Сообщение об успехе
            messages.success(request, f'Договор "{contract.number}" успешно создан!')
            
            # Перенаправляем на список
            return redirect('directories:contract_list')
    
    context = {
        'form': form,
        'page_title': 'Создать договор',
        'action': 'create',
    }
    
    return render(request, 'directories/contract_form.html', context)


@login_required
def contract_detail(request, pk):
    """
    Просмотр деталей договора.
    """
    contract = get_object_or_404(Contract.objects.select_related('counterparty'), pk=pk)
    
    context = {
        'contract': contract,
        'page_title': 'Просмотр договора',
    }
    
    return render(request, 'directories/contract_detail.html', context)


@login_required
def contract_update(request, pk):
    """
    Редактирование договора.
    """
    # Получаем объект или 404
    contract = get_object_or_404(Contract.objects.select_related('counterparty'), pk=pk)
    
    form = ContractForm(request.POST or None, instance=contract)
    
    if request.method == 'POST':
        if form.is_valid():
            contract = form.save(commit=False)
            contract.created_by = request.user  # Обновляем кто изменил
            contract.save()
            
            messages.success(request, f'Договор "{contract.number}" успешно обновлён!')
            return redirect('directories:contract_list')
    
    context = {
        'form': form,
        'contract': contract,
        'page_title': 'Редактировать договор',
        'action': 'update',
    }
    
    return render(request, 'directories/contract_form.html', context)


@login_required
def contract_delete(request, pk):
    """
    Мягкое удаление договора (soft delete).
    """
    contract = get_object_or_404(Contract, pk=pk)
    
    if request.method == 'POST':
        contract.archive()  # Мягкое удаление через метод модели
        
        messages.success(request, f'Договор "{contract.number}" успешно удалён!')
        return redirect('directories:contract_list')
    
    context = {
        'contract': contract,
        'page_title': 'Удалить договор',
    }
    
    return render(request, 'directories/contract_confirm_delete.html', context)


# =============================================================================
# ResponsiblePerson (Ответственные лица) - CRUD Views
# =============================================================================

@login_required
def responsible_person_list(request):
    """
    Список ответственных лиц с поиском и фильтрацией.
    """
    # Получаем все неархивированные ответственные лица
    persons = ResponsiblePerson.objects.all().order_by('last_name', 'first_name')
    
    # Поиск по фамилии, имени или должности
    search_query = request.GET.get('q', '')
    if search_query:
        persons = persons.filter(
            Q(last_name__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(position__icontains=search_query)
        )
    
    context = {
        'persons': persons,
        'search_query': search_query,
        'page_title': 'Ответственные лица',
    }
    
    return render(request, 'directories/responsible_person_list.html', context)


@login_required
def responsible_person_create(request):
    """
    Создание нового ответственного лица.
    """
    form = ResponsiblePersonForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            # Сохраняем объект, но не коммитим в БД сразу
            person = form.save(commit=False)
            person.created_by = request.user  # Запоминаем кто создал
            person.save()
            
            # Сообщение об успехе
            messages.success(request, f'Ответственное лицо "{person}" успешно создано!')
            
            # Перенаправляем на список
            return redirect('directories:responsible_person_list')
    
    context = {
        'form': form,
        'page_title': 'Создать ответственное лицо',
        'action': 'create',
    }
    
    return render(request, 'directories/responsible_person_form.html', context)


@login_required
def responsible_person_detail(request, pk):
    """
    Просмотр деталей ответственного лица.
    """
    person = get_object_or_404(ResponsiblePerson, pk=pk)
    
    context = {
        'person': person,
        'page_title': 'Просмотр ответственного лица',
    }
    
    return render(request, 'directories/responsible_person_detail.html', context)


@login_required
def responsible_person_update(request, pk):
    """
    Редактирование ответственного лица.
    """
    # Получаем объект или 404
    person = get_object_or_404(ResponsiblePerson, pk=pk)
    
    form = ResponsiblePersonForm(request.POST or None, instance=person)
    
    if request.method == 'POST':
        if form.is_valid():
            person = form.save(commit=False)
            person.created_by = request.user  # Обновляем кто изменил
            person.save()
            
            messages.success(request, f'Ответственное лицо "{person}" успешно обновлено!')
            return redirect('directories:responsible_person_list')
    
    context = {
        'form': form,
        'person': person,
        'page_title': 'Редактировать ответственное лицо',
        'action': 'update',
    }
    
    return render(request, 'directories/responsible_person_form.html', context)


@login_required
def responsible_person_delete(request, pk):
    """
    Мягкое удаление ответственного лица (soft delete).
    """
    person = get_object_or_404(ResponsiblePerson, pk=pk)
    
    if request.method == 'POST':
        person.archive()  # Мягкое удаление через метод модели
        
        messages.success(request, f'Ответственное лицо "{person}" успешно удалено!')
        return redirect('directories:responsible_person_list')
    
    context = {
        'person': person,
        'page_title': 'Удалить ответственное лицо',
    }
    
    return render(request, 'directories/responsible_person_confirm_delete.html', context)


# =============================================================================
# PowerOfAttorney (Доверенности) - CRUD Views
# =============================================================================

@login_required
def power_of_attorney_list(request):
    """
    Список доверенностей с поиском и фильтрацией.
    """
    # Получаем все неархивированные доверенности с связанными лицами
    powers = PowerOfAttorney.objects.select_related('responsible_person').all().order_by('-date', 'number')
    
    # Поиск по номеру или ФИО ответственного лица
    search_query = request.GET.get('q', '')
    if search_query:
        powers = powers.filter(
            Q(number__icontains=search_query) |
            Q(responsible_person__last_name__icontains=search_query) |
            Q(responsible_person__first_name__icontains=search_query)
        )
    
    context = {
        'powers': powers,
        'search_query': search_query,
        'page_title': 'Доверенности',
    }
    
    return render(request, 'directories/power_of_attorney_list.html', context)


@login_required
def power_of_attorney_create(request):
    """
    Создание новой доверенности.
    """
    form = PowerOfAttorneyForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            # Сохраняем объект, но не коммитим в БД сразу
            power = form.save(commit=False)
            power.created_by = request.user  # Запоминаем кто создал
            power.save()
            
            # Сообщение об успехе
            messages.success(request, f'Доверенность "{power.number}" успешно создана!')
            
            # Перенаправляем на список
            return redirect('directories:power_of_attorney_list')
    
    context = {
        'form': form,
        'page_title': 'Создать доверенность',
        'action': 'create',
    }
    
    return render(request, 'directories/power_of_attorney_form.html', context)


@login_required
def power_of_attorney_detail(request, pk):
    """
    Просмотр деталей доверенности.
    """
    power = get_object_or_404(
        PowerOfAttorney.objects.select_related('responsible_person'), 
        pk=pk
    )
    
    context = {
        'power': power,
        'page_title': 'Просмотр доверенности',
    }
    
    return render(request, 'directories/power_of_attorney_detail.html', context)


@login_required
def power_of_attorney_update(request, pk):
    """
    Редактирование доверенности.
    """
    # Получаем объект или 404
    power = get_object_or_404(
        PowerOfAttorney.objects.select_related('responsible_person'), 
        pk=pk
    )
    
    form = PowerOfAttorneyForm(request.POST or None, instance=power)
    
    if request.method == 'POST':
        if form.is_valid():
            power = form.save(commit=False)
            power.created_by = request.user  # Обновляем кто изменил
            power.save()
            
            messages.success(request, f'Доверенность "{power.number}" успешно обновлена!')
            return redirect('directories:power_of_attorney_list')
    
    context = {
        'form': form,
        'power': power,
        'page_title': 'Редактировать доверенность',
        'action': 'update',
    }
    
    return render(request, 'directories/power_of_attorney_form.html', context)


@login_required
def power_of_attorney_delete(request, pk):
    """
    Мягкое удаление доверенности (soft delete).
    """
    power = get_object_or_404(PowerOfAttorney, pk=pk)
    
    if request.method == 'POST':
        power.archive()  # Мягкое удаление через метод модели
        
        messages.success(request, f'Доверенность "{power.number}" успешно удалена!')
        return redirect('directories:power_of_attorney_list')
    
    context = {
        'power': power,
        'page_title': 'Удалить доверенность',
    }
    
    return render(request, 'directories/power_of_attorney_confirm_delete.html', context)


# =============================================================================
# HTMX Partials (для модальных окон выбора)
# =============================================================================

@login_required
def htmx_counterparty_search(request):
    """
    HTMX поиск контрагентов для модального окна.
    Возвращает HTML partial с результатами поиска.
    """
    search_query = request.GET.get('q', '')
    
    # Получаем контрагентов с поиском
    counterparties = Counterparty.objects.all().order_by('name')
    
    if search_query:
        counterparties = counterparties.filter(
            Q(name__icontains=search_query) |
            Q(inn__icontains=search_query) |
            Q(email__icontains=search_query)
        )[:50]  # Ограничиваем результат для производительности
    
    context = {
        'counterparties': counterparties,
        'search_query': search_query,
    }
    
    # Возвращаем только partial шаблон (без base.html)
    return render(request, 'directories/partials/counterparty_search_results.html', context)


@login_required
def htmx_contract_search(request):
    """
    HTMX поиск договоров для модального окна.
    Возвращает HTML partial с результатами поиска.
    """
    search_query = request.GET.get('q', '')
    
    # Получаем договоры с поиском и связанными контрагентами
    contracts = Contract.objects.select_related('counterparty').all().order_by('-date', 'number')
    
    if search_query:
        contracts = contracts.filter(
            Q(number__icontains=search_query) |
            Q(counterparty__name__icontains=search_query)
        )[:50]  # Ограничиваем результат
    
    context = {
        'contracts': contracts,
        'search_query': search_query,
    }
    
    return render(request, 'directories/partials/contract_search_results.html', context)


@login_required
def htmx_responsible_person_search(request):
    """
    HTMX поиск ответственных лиц для модального окна.
    Возвращает HTML partial с результатами поиска.
    """
    search_query = request.GET.get('q', '')
    
    # Получаем ответственных лиц с поиском
    persons = ResponsiblePerson.objects.all().order_by('last_name', 'first_name')
    
    if search_query:
        persons = persons.filter(
            Q(last_name__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(position__icontains=search_query)
        )[:50]  # Ограничиваем результат
    
    context = {
        'persons': persons,
        'search_query': search_query,
    }
    
    return render(request, 'directories/partials/responsible_person_search_results.html', context)


@login_required
def htmx_power_of_attorney_search(request):
    """
    HTMX поиск доверенностей для модального окна.
    Возвращает HTML partial с результатами поиска.
    """
    search_query = request.GET.get('q', '')
    
    # Получаем доверенности с поиском и связанными лицами
    powers = PowerOfAttorney.objects.select_related('responsible_person').all().order_by('-date', 'number')
    
    if search_query:
        powers = powers.filter(
            Q(number__icontains=search_query) |
            Q(responsible_person__last_name__icontains=search_query) |
            Q(responsible_person__first_name__icontains=search_query)
        )[:50]  # Ограничиваем результат для производительности
    
    context = {
        'powers': powers,
        'search_query': search_query,
    }
    
    return render(request, 'directories/partials/power_of_attorney_search_results.html', context)


@login_required
def htmx_work_type_search(request):
    """
    HTMX поиск видов работ для модального окна.
    Возвращает HTML partial с результатами поиска.
    """
    search_query = request.GET.get('q', '')
    
    # Получаем виды работ с поиском
    work_types = WorkType.objects.all().order_by('full_name')
    
    if search_query:
        work_types = work_types.filter(
            Q(full_name__icontains=search_query) |
            Q(short_name__icontains=search_query)
        )[:50]  # Ограничиваем результат
    
    context = {
        'work_types': work_types,
        'search_query': search_query,
    }
    
    return render(request, 'directories/partials/work_type_search_results.html', context)


@login_required
def htmx_unit_search(request):
    """
    HTMX поиск единиц измерения для модального окна.
    Возвращает HTML partial с результатами поиска.
    """
    search_query = request.GET.get('q', '')
    
    # Получаем единицы измерения с поиском
    units = Unit.objects.all().order_by('full_name')
    
    if search_query:
        units = units.filter(
            Q(full_name__icontains=search_query) |
            Q(short_name__icontains=search_query)
        )[:50]  # Ограничиваем результат
    
    context = {
        'units': units,
        'search_query': search_query,
    }
    
    return render(request, 'directories/partials/unit_search_results.html', context)