import uuid
from django.db import models
from django.db import models, IntegrityError, transaction
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.password_validation import validate_password

# Custom user manager to create admin superuser
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        
        email = self.normalize_email(email).lower().strip()
        extra_fields.setdefault("is_active", True)

        user = self.model(email=email, **extra_fields)
        if password:
            validate_password(password, user=user)
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

# User class
class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )

    # Email as primary identifier
    email = models.EmailField(unique=True, db_index=True)
    is_email_verified = models.BooleanField(default=False)

    # Username (defaults to the email, editable later)
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=True
    )
    

    # Names
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=True
    )

    # Integration context for Yiyara Decomposer & Scheduler
    google_refresh_token = models.TextField(blank=True, null=True)
    calendar_sync_enabled = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # Attach custom user manager to user
    objects = UserManager()

    class Meta:
        ordering = ['email']

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower().strip()

        # Auto-generate username from email
        if not self.username:
            base_username = self.email.split("@")[0]
            candidate = base_username
            counter = 1
            max_attempts = 10

            for attempts in range(max_attempts):
                self.username = candidate
                try:
                    with transaction.atomic():
                        super().save(*args, **kwargs)
                    return
                except IntegrityError:
                    counter += 1
                    candidate = f"{base_username}{counter}"

            raise IntegrityError(
                f"Could not generate a unique username for {self.email} "
                f"after {max_attempts} attempts."
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
    
