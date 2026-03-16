from django.db import models
from apps.core.models import BaseModel


class WorkType(BaseModel):
    """
    Справочник видов работ.    
    """
    
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