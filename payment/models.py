from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, matric_number, email, password=None, **extra_fields):
        if not matric_number:
            raise ValueError('The Matric Number must be set')
        email = self.normalize_email(email)
        user = self.model(matric_number=matric_number, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, matric_number, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(matric_number, email, password, **extra_fields)

class User(AbstractUser):
    matric_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'matric_number'
    REQUIRED_FIELDS = ['email', 'first_name']

    def __str__(self):
        return self.matric_number

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference_number = models.CharField(max_length=20, unique=True)
    payment_method = models.CharField(max_length=20, choices=[('card', 'Card'), ('bank_transfer', 'Bank Transfer')])
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.reference_number} by {self.user.matric_number}"
