from datetime import date
from django.db import models
from django.contrib.auth.models import User, BaseUserManager, AbstractBaseUser



class CustomUserManager(BaseUserManager):
    # id = models.IntegerField(primary_key=True)
    def create_user(self, email, date_of_birth, password=None):
        
        if not email:
            raise ValueError("Users must get a mail adress")
        
        user = self.model(email=self.normalize_email(email), date_of_birth=date_of_birth)
        user.set_password(self.password)
        user.save()
        return user
    
    def create_superuser(self, email, password=None, date_of_birth=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        user = self.create_user(email, password=password, date_of_birth=date_of_birth, **extra_fields)
        # user.is_admin = True
        user.save()
        return user
           
class CustomUser(AbstractBaseUser):
    email = models.EmailField(name="email", max_length=255, unique=True)
    
    class UserGroupe(models.TextChoices):
        SALE = "Sale", "Sale role"
        SUPPORT = "Support", "Support role"
        MANAGEMENT = "Management", "Management role"
        DEFAULT = "Default", "Not assigned"
        
    usergroup = models.CharField(UserGroupe, max_length=15, choices=UserGroupe.choices, default=UserGroupe.MANAGEMENT)
    date_of_birth = models.DateField(default=date.today, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        verbose_name = "User"
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
    # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    def __str__(self):
        return self.email
        

        


