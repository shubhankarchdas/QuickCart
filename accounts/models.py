from venv import logger
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from datetime import timedelta

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, phone_number, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        
        # Check for existing unverified user first
        try:
            existing_user = self.get(email=email, is_active=False)
            return existing_user  # Return existing unverified user
        except self.model.DoesNotExist:
            pass  # Proceed with creation
        
        # Create new user
        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            is_active=False  # New users are inactive by default
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_unverified_user(self, email):
        """Safely get unverified user or None"""
        try:
            return self.get(email=email, is_active=False)
        except Account.DoesNotExist:
            return None
        except Exception as e:
            logger.error(f"Error fetching unverified user: {str(e)}")
            return None
        

    def create_superuser(self, email, username, first_name, last_name, password=None):
        user = self.create_user(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user



class Account(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=15)

    last_activation_sent = models.DateTimeField(null=True, blank=True)
    activation_attempts = models.PositiveIntegerField(default=0)
    activation_locked_until = models.DateTimeField(null=True, blank=True)

    # Standard fields
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)  # Changed default to False
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return f"{self.email}, ID: {self.id}, Created at: {self.created_at}, Active: {self.is_active}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


    def can_send_activation(self):
        """Check if activation email can be sent"""
        # Check if account is locked
        if self.activation_locked_until and self.activation_locked_until > timezone.now():
            remaining_time = (self.activation_locked_until - timezone.now()).seconds // 60
            return False, f"Please wait {remaining_time} minutes before trying again"
        
        # Check attempt limit
        if self.activation_attempts >= 3:
            self.activation_locked_until = timezone.now() + timedelta(minutes=5)
            self.save()
            return False, "Maximum attempts reached. Please wait 5 minutes."
        
        return True, None

    def reset_activation_attempts(self):
        """Reset activation attempts and lock"""
        self.activation_attempts = 0
        self.activation_locked_until = None
        self.save()


    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    




    