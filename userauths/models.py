from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator


USER_TYPE = (
    ('Vendor', 'Vendor'),
    ('Customer', 'Customer'),
)


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (instance.user.username, filename)
    return 'user_{0}/{1}'.format(instance.user.username, filename)


class User(AbstractUser):
    username = models.CharField(unique=True, max_length=100)
    email = models.EmailField(unique=True, validators=[EmailValidator()])

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def clean(self):
        super().clean()
        if not self.username:
            self.username = self.email.split('@')[0]

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username or self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to=user_directory_path, default='default-profile.jpg', null=True, blank=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=50, null=True, blank=True)
    user_type = models.CharField(max_length=50, choices=USER_TYPE, default='Customer')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return self.user.username or str(self.user)