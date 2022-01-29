from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class User(AbstractUser):
    FORBIDDEN_USERNAME = [
        'me', 'Me',
        'admin', 'Admin'
    ]
    ERROR_FORBIDDEN_USERNAME = ('Использовать имя "{username}" в качестве '
                                'username запрещено.')

    def save(self, *args, **kwargs):
        if self.username in self.FORBIDDEN_USERNAME and not self.is_superuser:
            raise ValidationError(
                self.ERROR_FORBIDDEN_USERNAME.format(username=self.username)
            )
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-username', '-date_joined']
