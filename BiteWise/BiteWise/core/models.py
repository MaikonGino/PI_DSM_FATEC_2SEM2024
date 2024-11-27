from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


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

        if not extra_fields.get('is_staff'):
            raise ValueError("Superusuários precisam ter is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superusuários precisam ter is_superuser=True.")

        return self.create_user(email, password, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, blank=True, null=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    google_id = models.CharField(max_length=255, blank=True, null=True, unique=True)  
    profile_picture = models.URLField(blank=True, null=True)  
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        db_table = 'usuario'  

    def __str__(self):
        return self.email

class Receita(models.Model):
    id_receita = models.IntegerField(unique=True)  
    titulo = models.CharField(max_length=255)
    titulo_traduzido = models.CharField(max_length=255, blank=True, null=True)
    imagem = models.URLField(max_length=500, blank=True, null=True)
    tempo_preparo = models.IntegerField(blank=True, null=True)  
    tempo_total = models.IntegerField(blank=True, null=True)  
    porcoes = models.IntegerField(blank=True, null=True)
    dificuldade = models.CharField(max_length=50, blank=True, null=True)
    dicas = models.TextField(blank=True, null=True)
    dicas_traduzidas = models.TextField(blank=True, null=True)
    instrucoes = models.TextField(blank=True, null=True)
    instrucoes_traduzidas = models.TextField(blank=True, null=True)

    data_criacao = models.DateTimeField(auto_now_add=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

class IngredienteReceita(models.Model):
    receita = models.ForeignKey(Receita, related_name='ingredientes', on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    nome_traduzido = models.CharField(max_length=255, blank=True, null=True)
    quantidade = models.FloatField(blank=True, null=True)
    unidade = models.CharField(max_length=50, blank=True, null=True)
    unidade_traduzida = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.quantidade} {self.unidade} de {self.nome}"
