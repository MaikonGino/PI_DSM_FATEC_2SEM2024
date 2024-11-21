from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth import get_user_model
from allauth.socialaccount.models import SocialAccount



# Create your models here.
class Ingrediente(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    imagem = models.FileField(upload_to='ingredientes/')

    def __str__(self):
        return self.nome

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True, blank=True, null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    
    # Campos relacionados ao Google
    google_id = models.CharField(max_length=255, blank=True, null=True, unique=True)  # ID do Google
    profile_picture = models.URLField(blank=True, null=True)  # Foto de perfil do Google
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        db_table = 'usuario'  # A tabela será a mesma para CustomUser

    def __str__(self):
        return self.email