from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.

LISTA_CATEGORIAS = (
    ("ANALISES", "Análises"),
    ("PROGRAMACAO", "Programação"),
    ("APRESENTACAO", "Apresentação"),
    ("OUTROS", "Outros")
)
#criar o filme
class Filme(models.Model):
    titulo = models.CharField(max_length=200)
    thumb = models.ImageField(upload_to='thumb_filmes')
    descricao = models.TextField(max_length=1000)
    categoria = models.CharField(max_length=20, choices=LISTA_CATEGORIAS)
    visualizacoes = models.IntegerField(default=0)
    data_criacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.titulo

# criar os episodios
class Episodio(models.Model):
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE, related_name='episodios')
    titulo = models.CharField(max_length=200)
    video = models.URLField()

    def __str__(self):
        return self.filme.titulo + ' - ' + self.titulo


class Usuario(AbstractUser):
    filmes_vistos = models.ManyToManyField("Filme")