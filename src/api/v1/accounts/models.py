
import uuid
from django.core.mail import send_mail
from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from .managers import CustomUserManager
from .services import get_path_upload_avatar


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Кастомный юзер сайта для чтения манги, имеет:
        Юзернейм;
        Почту;
        Является ли сотрудником(is_stuff);
        Ялвяется ли активыным;
        Дата создания аккаунта;
        Баланс;
        Пол;
        Фото пользователя;
        О себе;
    """

    SEX = (
        ('М', 'Мужской'),
        ('Ж', 'Женский')
    )

    username = models.CharField(
        "username",
        max_length=150,
        unique=True,
        help_text=
        "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ,
        error_messages={
            "unique": "Пользователь с таким именем уже существует",
        },
    )
    email = models.EmailField("email address",
                              max_length=150,
                              unique=True,
                              error_messages={
                                  "unique": "Пользователь с таким email уже существует",
                              }
                              )

    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site."
    )
    is_active = models.BooleanField(
        "active",
        default=True,
        help_text="Designates whether this user should be treated as active. "
                  "Unselect this instead of deleting accounts."
    )
    created = models.DateTimeField('Дата создания аккаунта', default=timezone.now)

    sex = models.CharField('Пол пользователя', choices=SEX, default=None, null=True)

    balance = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    avatar = models.ImageField(
        'Фото профиля',
        upload_to=get_path_upload_avatar,
        default='avatars/default.png',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])])

    descriptions = models.CharField('О себе', max_length=500, null=True, blank=True)

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)
