from django.db import models


from django.db import models
from django.conf import settings
from django.utils import timezone


class SoftDeleteManager(models.Manager):
    """
    Менеджер для мягкого удаления.    
    Возвращает только НЕ архивированные записи. Например: objects = SoftDeleteManager()    

    Как работает? super().get_queryset() вызывает метод родительского класса (models.Manager), 
    который возвращает обычный QuerySet, содержащий все записи модели.
    Затем мы применяем к этому QuerySet фильтр .filter(is_archived=False), 
    который оставляет только записи, не находящиеся в архиве.

    Что возвращает? QuerySet, в котором уже «вшит» фильтр по is_archived=False. 
    Теперь любые запросы через этот менеджер (например, .all(), .filter(...)) 
    будут автоматически учитывать это условие.
    """
    def get_queryset(self):
        return super().get_queryset().filter(is_archived=False)


class BaseModel(models.Model):
    """
    Базовая модель с soft delete и аудитом.
    Наследуется от Django Model, является абстрактной.

    Все Модели, наследуемые от этой модели автоматически получает поля:
    is_archived, created_at, updated_at, created_by, 
    а также методы: archive(), restore(), hard_delete()
    и менеджеры: objects (только неархивированные) и all_objects (все)
    """
    
    # Поле мягкого удаления
    is_archived = models.BooleanField(
        default=False, # по умолчанию новые записи не архивированы
        db_index=True, # создаёт индекс в базе данных для этого поля, чтобы ускорить поиск и фильтрацию по нему
        verbose_name="Архивировано"
    )
    
    # Поля аудита (даты)
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения"
    )
    
    # Поле аудита (пользователь)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # если пользователь будет удалён, то в этом поле станет NULL (запись не удалится)
        null=True,
        blank=True,
        related_name='%(class)s_created',
        verbose_name="Создал"
    )
    
    # Менеджеры модели
    objects = SoftDeleteManager()      # По умолчанию скрывает архивированные, 
    all_objects = models.Manager()     # Показывает ВСЕ записи
    
    class Meta:
        abstract = True                # Не создаёт таблицу в БД, служит только для передачи полей и методов дочерним моделям.
        ordering = ['-created_at']     # Сортировка по умолчанию
    
    # Методы модели
    def archive(self):
        """Мягкое удаление (архивация)"""
        self.is_archived = True
        self.save(update_fields=['is_archived', 'updated_at'])
    
    def restore(self):
        """Восстановление из архива"""
        self.is_archived = False
        self.save(update_fields=['is_archived', 'updated_at'])
    
    def hard_delete(self):
        """Полное удаление (обход менеджера)"""
        self.all_objects.filter(pk=self.pk).delete()
    
    def __str__(self):
        """Строковое представление (переопределяется в дочерних моделях)"""
        return f"{self.__class__.__name__} #{self.pk}"
