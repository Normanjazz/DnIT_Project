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