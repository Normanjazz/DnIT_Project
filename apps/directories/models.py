from django.db import models
from apps.core.models import BaseModel


class WorkType(BaseModel):
    """
    Справочник видов работ.
    """

    # ВЫБОР ОРГАНИЗАЦИИ
    ORGANIZATION_TYPE_CHOICES = [
        ('GC', 'ГК (Группа компаний)'),
        ('CHOU', 'ЧОУ (Частное образовательное учреждение)'),
    ]

    # ПОЛЕ ТИПА ОРГАНИЗАЦИИ
    organization_type = models.CharField(
        max_length=10,
        choices=ORGANIZATION_TYPE_CHOICES,
        verbose_name="Тип организации"
    )

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
        ordering = ['organization_type', 'full_name']
        indexes = [
            models.Index(fields=['organization_type']),
            models.Index(fields=['full_name']),
        ]

    def __str__(self):
        return self.full_name
    

class Unit(BaseModel):
    """
    Справочник для единиц измерения
    """
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
        # Возвращаем сокращённое имя, если есть, иначе полное
        return self.short_name or self.full_name

class Counterparty(BaseModel):
    """
    Справочник для контрагентов
    """

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
    

class Contract(BaseModel):
    """
    Справочник договоров. Связан с контрагентом (один ко многим).
    """

    # ВЫБОР ОРГАНИЗАЦИИ
    ORGANIZATION_TYPE_CHOICES = [
        ('GC', 'ГК (Группа компаний)'),
        ('CHOU', 'ЧОУ (Частное образовательное учреждение)'),
    ]

    # ПОЛЕ ТИПА ОРГАНИЗАЦИИ
    organization_type = models.CharField(
        max_length=10,
        choices=ORGANIZATION_TYPE_CHOICES,
        verbose_name="Тип организации"
    )

    number = models.CharField(
        max_length=50,
        verbose_name="Номер договора"
    )

    date = models.DateField(
        verbose_name="Дата договора"
    )

    # Связь с контрагентом
    counterparty = models.ForeignKey(
        Counterparty,
        on_delete=models.PROTECT,  # Нельзя удалить контрагента, если есть договоры
        related_name='contracts',  # Доступ через counterparty.contracts.all()
        verbose_name="Контрагент"
    )

    class Meta:
        verbose_name = "Договор"
        verbose_name_plural = "Договоры"
        ordering = ['-date', 'number']
        unique_together = ['organization_type', 'number', 'date']  # Уникальность пары номер+дата + организация
        indexes = [
            models.Index(fields=['organization_type']),
            models.Index(fields=['number']),
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return f"{self.number} от {self.date.strftime('%d.%m.%Y')}"
    

class ResponsiblePerson(BaseModel):
    """
    Справочник ответственных лиц.
    Используется в доверенностях для указания кому выдана доверенность.
    """
    
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


class PowerOfAttorney(BaseModel):
    """
    Справочник доверенностей.
    Связан с ответственным лицом (один ко многим).
    Используется в счетах для указания лица, действующего от имени организации.
    """

    # ВЫБОР ОРГАНИЗАЦИИ
    ORGANIZATION_TYPE_CHOICES = [
        ('GC', 'ГК (Группа компаний)'),
        ('CHOU', 'ЧОУ (Частное образовательное учреждение)'),
    ]

    # ПОЛЕ ТИПА ОРГАНИЗАЦИИ
    organization_type = models.CharField(
        max_length=10,
        choices=ORGANIZATION_TYPE_CHOICES,
        verbose_name="Тип организации"
    )

    number = models.CharField(
        max_length=50,
        verbose_name="Номер доверенности"
    )

    date = models.DateField(
        verbose_name="Дата доверенности"
    )

    # Связь с ответственным лицом
    responsible_person = models.ForeignKey(
        ResponsiblePerson,
        on_delete=models.PROTECT,  # Нельзя удалить лицо, если есть доверенности
        related_name='powers_of_attorney',  # Доступ через person.powers_of_attorney.all()
        verbose_name="Ответственное лицо"
    )

    class Meta:
        verbose_name = "Доверенность"
        verbose_name_plural = "Доверенности"
        ordering = ['-date', 'number']
        unique_together = ['organization_type', 'number', 'date']  # Уникальность пары номер+дата + организация
        indexes = [
            models.Index(fields=['organization_type']),
            models.Index(fields=['number']),
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return f"№{self.number} от {self.date.strftime('%d.%m.%Y')}"
    

