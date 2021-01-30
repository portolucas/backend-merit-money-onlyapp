from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.


class Cargo(models.Model):
    descricao = models.CharField(max_length=51, null=True)

    def __str__(self):
        return (self.descricao) 


class Setor(models.Model):
    descricao = models.CharField(max_length=50, null=True)

    def __str__(self):
        return (self.descricao)


class Premios(models.Model):
    descricao = models.CharField(max_length=50, null=True)
    valor = models.IntegerField(null=True)
    
    def __str__(self):
        return (self.descricao)


class Transacao(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    data_transacao = models.DateField(blank=True, null=True)
    id_remetente = models.IntegerField()
    id_destinatario = models.IntegerField()
    valor = models.IntegerField()
    justificativa = models.CharField(max_length=100)
    
class TransacaoPremios(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    data_transacao = models.DateField(blank=True, null=True)
    premio_resgatado = models.IntegerField()
    id_colaborador = models.IntegerField()


class Colaborador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50)
    cargo = models.ForeignKey(
        Cargo, related_name='cargo_colaborador',  on_delete=models.RESTRICT, null=True)
    setor = models.ForeignKey(
        Setor, related_name='setor_colaborador',  on_delete=models.RESTRICT, null=True)
    saldo_acumulado = models.IntegerField()
    saldo_recebido = models.IntegerField(null=True)
    premios = models.ManyToManyField(
        Premios, related_name='premios_colaborador', blank=True)


    def __str__(self):
        return (self.nome)

