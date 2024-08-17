from django.contrib.auth.models import AbstractUser
from django.db import models

from product.courses.models import Course


class CustomUser(AbstractUser):
    """Кастомная модель пользователя - студента."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=250,
        unique=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.get_full_name()


class Balance(models.Model):
    """Модель баланса пользователя."""

    # TODO +
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1000, verbose_name='Баланс')


    def save(self, *args, **kwargs):
        if self.amount < 0:
            raise ValueError("Баланс не может быть ниже 0")
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
        ordering = ('-id',)

    class Group(models.Model):
        """Модель группы."""

        # TODO +
        title = models.CharField(max_length=250, verbose_name='Название группы')
        course = models.ForeignKey(Course, related_name='groups', on_delete=models.CASCADE, verbose_name='Курс')
        students = models.ManyToManyField(User, related_name='groups', blank=True, verbose_name='Студенты')

        class Meta:
            verbose_name = 'Группа'
            verbose_name_plural = 'Группы'
            ordering = ('-id',)

        def str(self):
            return f'{self.title} ({self.course.title})'
