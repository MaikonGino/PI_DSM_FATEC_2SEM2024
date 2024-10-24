from django.db import models

# Create your models here.
class Ingrediente(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    imagem = models.FileField(upload_to='ingredientes/')

    def __str__(self):
        return self.nome