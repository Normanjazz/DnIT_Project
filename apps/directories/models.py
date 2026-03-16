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