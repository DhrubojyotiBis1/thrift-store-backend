from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser,BaseUserManager
from django.contrib.auth.models import PermissionsMixin

from teams.models import Teams

class GamerManagers(BaseUserManager):

    def _save(self, gamer):
        gamer.save(using=self._db)

    def _create_user(self, email, phone, first_name, last_name, photo_url, team, is_active, is_staff=False, is_superuser=False):
        if not email:
            raise ValueError('Email Required')
        if not first_name:
            raise ValueError('First Name Required')
        email = self.normalize_email(email)
        gamer = self.model(
            email=email, 
            phone=phone, 
            first_name=first_name, 
            last_name=last_name, 
            photo_url=photo_url, 
            team=team, 
            is_staff=is_staff, 
            is_active=is_active, 
            is_superuser=is_superuser
        )
        self._save(gamer)
        return gamer

    def create_user(self, email, phone, first_name, last_name, photo_url=None, team=None, is_active=True):
        return self._create_user(
            email=email, 
            phone=phone, 
            first_name=first_name, 
            last_name=last_name, 
            photo_url=photo_url, 
            team=team, 
            is_active=is_active, 
        )

    def create_superuser(self, email, phone, first_name, last_name, photo_url=None, team=None, is_active=True):
        return self._create_user(
            email=email, 
            phone=phone, 
            first_name=first_name, 
            last_name=last_name, 
            photo_url=photo_url, 
            team=team, 
            is_staff=True, 
            is_active=is_active, 
            is_superuser=True
        )
    
class Gamers(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True,max_length=255)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50,blank=True, null=True)
    photo_url = models.CharField(max_length=150,blank=True)
    phone = models.CharField(unique=True,max_length=20,blank=True)
    team = models.ForeignKey(Teams, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True)

    is_staff = models.BooleanField('staff status',default=False)
    is_active = models.BooleanField('active',default=False)
    is_superuser = models.BooleanField('superuser',default=False)

    groups = models.ManyToManyField('auth.Group', related_name='gamers_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='gamers_permissions_set', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'phone']

    objects = GamerManagers()

    def __str__(self):
        return self.email

    def full_name(self):
        # Handle cases where last name might be blank
        return f"{self.first_name} {self.last_name}".strip()

    def has_perm(self, perm, obj=None):
        # Allow all permissions for superusers
        if self.is_superuser:
            return True
        return super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        # Allow all module permissions for superusers
        if self.is_superuser:
            return True
        return super().has_module_perms(app_label)