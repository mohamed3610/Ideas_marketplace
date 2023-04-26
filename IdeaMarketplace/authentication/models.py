from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

# Create your models here.


def validate_email_domain(value):
    allowed_domain = 'ecs-co.com'
    email_domain = value.split('@')[1]
    if email_domain != allowed_domain:
        raise ValidationError('Only email addresses from ecs-co.com domain are allowed.')


class Employee(AbstractUser):
    email = models.EmailField(validators=[EmailValidator(message='Invalid email format,Only email addresses from ecs-co.com domain are allowed.'), validate_email_domain])

    def __str__(self):
        return self.username