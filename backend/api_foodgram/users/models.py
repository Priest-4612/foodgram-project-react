from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


class User(AbstractUser):
    FORBIDDEN_USERNAME = [
        'me', 'Me',
        'admin', 'Admin'
    ]
    ERROR_FORBIDDEN_USERNAME = ('Использовать имя "{username}" в качестве '
                                'username запрещено.')

    email = models.EmailField(
        db_index=True,
        unique=True,
        max_length=254,
        blank=False
    )
    first_name = models.CharField(
        max_length=150,
        blank=False,
    )
    last_name = models.CharField(
        max_length=150,
        blank=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        ordering = ['-username', '-date_joined']

    def save(self, *args, **kwargs):
        if self.username in self.FORBIDDEN_USERNAME and not self.is_superuser:
            raise ValidationError(
                self.ERROR_FORBIDDEN_USERNAME.format(username=self.username)
            )
        super().save(*args, **kwargs)


class Subscribe(models.Model):
    subscriber = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='subscriber'
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='author'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['subscriber', 'author'],
                name='unique_author_user_following'
            )
        ]

    def __str__(self) -> str:
        return (
            f'Автор: {self.author} '
            f'- Подписчик: {self.subscriber}'
        )
