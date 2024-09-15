from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser,BaseUserManager
from django.contrib.auth.models import PermissionsMixin

class SponsorManagers(BaseUserManager):
    '''Manager for Sponsors Model'''

    def _save(self, sponsor):
        sponsor.save(using=self._db)
    
    def _create_user(self, email, phone, first_name, last_name, company, is_staff, is_active, is_superuser):
        if not email:
            raise ValueError('Email Required')
        if not first_name:
            raise ValueError('First Name Required')
        email = self.normalize_email(email)
        sponsor = self.model(
            email=email, 
            phone=phone, 
            first_name=first_name, 
            last_name=last_name, 
            company=company,
            is_staff=is_staff, 
            is_active=is_active, 
            is_superuser=is_superuser
        )
        self._save(sponsor)
        return sponsor

    def create_user(self, email, phone, first_name, last_name, company, is_active=True):
        return self._create_user(
            email=email, 
            phone=phone, 
            first_name=first_name, 
            last_name=last_name, 
            company=company,
            is_active=is_active, 
        )

    def create_superuser(self, email, phone, first_name, last_name, company, is_active=True):
        return self._create_user(
            email=email, 
            phone=phone, 
            first_name=first_name, 
            last_name=last_name, 
            company=company,
            is_active=is_active, 
            is_staff=True, 
            is_superuser=True
        )

class Sponsors(AbstractBaseUser, PermissionsMixin):
    '''Database model for Sponsors in the system'''

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50,blank=True)
    company = models.CharField(max_length=255,null=False, default='')
    email = models.EmailField(unique=True,max_length=255,blank=False)
    phone = models.CharField(max_length=20,blank=True,unique=True,)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True)

    is_staff = models.BooleanField('staff status',default=False)
    is_active = models.BooleanField('active',default=False)
    is_superuser = models.BooleanField('superuser',default=False)

    groups = models.ManyToManyField('auth.Group',related_name='sponsors_set',blank=True)
    user_permissions = models.ManyToManyField('auth.Permission',related_name='sponsors_permissions_set',blank=True)

    objects = SponsorManagers()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'phone']

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
        
        