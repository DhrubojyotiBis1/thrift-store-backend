from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser,BaseUserManager
from django.contrib.auth.models import PermissionsMixin

# Create your models here.

class GamersManager(BaseUserManager):

    def _save(self, gamer):
        gamer.same(using=self._db)

    def _create_user(self, email, phone, first_name, last_name, photo_url, team_id, is_staff, is_active, is_superuser):
        if not email:
            raise ValueError('Email Required')
        if not first_name:
            raise ValueError('Name Required')
        email = self.normalize_email(email)
        gamer = self.model(email=email, phone=phone, first_name=first_name, last_name=last_name, photo_url=photo_url, 
                           team_id=team_id, is_staff=is_staff, is_active=is_active, is_superuser= is_superuser)
        self._save(gamer)
        return gamer
    
    def create_user(self, email, phone, first_name, last_name, photo_url, team_id, is_staff, is_active, is_superuser):
        return self._create_user(email=email, phone=phone, first_name=first_name, last_name=last_name, photo_url=photo_url, 
                                 team_id=team_id, is_staff=is_staff, is_active=is_active, is_superuser=is_superuser)
    
    def create_superuser(self, email, phone, first_name, last_name, photo_url, team_id, is_active=True):
        return self._create_user(email=email, phone=phone, first_name=first_name, last_name=last_name, photo_url=photo_url, 
                                 team_id=team_id, is_staff=True, is_active=is_active, is_superuser=True)
    
class Gamers(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True,max_length=255,blank=False)
    first_name = models.CharField('first_name',max_length=50,blank=False)
    last_name = models.CharField('last_name',max_length=50,blank=True)
    photo_url = models.CharField('photo_url',max_length=150,blank=True)
    phone = models.CharField('phone',max_length=20,blank=True)
    team_id = models.CharField('team_id',max_length=10,blank=True) # foreign key team-id


    is_staff = models.BooleanField('staff status',default=False)
    is_active = models.BooleanField('active',default=False)
    is_superuser = models.BooleanField('superuser',default=False)
  
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'phone']

    objects = GamersManager()

    def __str__(self):
        return self.email
    
    def full_name(self):
        return self.first_name+" "+self.last_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True