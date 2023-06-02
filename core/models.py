from datetime import date
from django.db import models
from django.contrib.auth.models import User, BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    id = models.IntegerField(primary_key=True)
    def create_user(self, email, date_of_birth, password=None):
        
        if not email:
            raise ValueError("Users must get a mail adress")
        
        user = self.model(email=self.normalize_email(email), date_of_birth=date_of_birth)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password=None, date_of_birth=None):
        user = self.create_user(email, password=password, date_of_birth=date_of_birth)
        user.is_admin = True
        user.save()
        return user
           
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email adress", max_length=255, unique=True)
    
    class UserGroupe(models.TextChoices):
        SALE = "Sale", "Sale role"
        SUPPORT = "Support", "Support role"
        MANAGEMENT = "Management", "Management role"
        DEFAULT = "Default", "Not assigned"
        
    usergroup = models.CharField(UserGroupe, max_length=15, choices=UserGroupe.choices, default=UserGroupe.DEFAULT)
    date_of_birth = models.DateField(default=date.today, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = "email"
    
    class Meta:
        verbose_name = "User"
    
    def __str__(self) -> str:
        return self.email
    
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
        
        


