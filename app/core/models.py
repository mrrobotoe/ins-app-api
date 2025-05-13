"""
Database models for the application.
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create and return a user with an email and password."""
        if not email:
            raise ValueError("Users must have an email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a new superuser with an email and password."""
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username."""

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Address(models.Model):
    """Address model."""
    address = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.address}, {self.city}, {self.state} {self.zip_code}"


class Client(models.Model):
    """Client model."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING
    )
    main_address = models.ForeignKey(
        Address,
        on_delete=models.DO_NOTHING,
    )
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Inspection(models.Model):
    """Inspection model."""

    inspector_name = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
    )
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    inspection_date = models.DateField()
    inspection_type = models.CharField(max_length=255)
    report_number = models.CharField(max_length=255)
    address = models.ForeignKey(
        Address,
        on_delete=models.DO_NOTHING
    )
    buyer_agent = models.CharField(max_length=255)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=50)
    signed_status = models.CharField(max_length=50)
    release_status = models.CharField(max_length=50)
    notes = models.TextField()

    def __str__(self):
        return f"{self.inspection_type} - {self.client.name}"
