from django.db import models

# Create your models here.

class modelClass(models.Model):
    active = models.BooleanField(default=True)
    create = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Categoria(modelClass):
    description = models.CharField(
        max_length = 100,
        help_text = 'Descripción de la categoria',
        unique = True
    )

    def __str__(self):
        return "{}".format(self.description)

    def save(self):
        self.description = self.description.upper()
        super(Categoria, self).save()

    class Meta:
        verbose_name_plural = "Categorias"

class SubCategoria(modelClass):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    description = models.CharField(
        max_length = 100,
        help_text = 'Descripción de la Sub Categoria',
    )

    def __str__(self):
        return "{}:{}".format(self.categoria.description, self.description)

    def save(self, *args, **kwargs):
        self.description = self.description.upper()
        super(Categoria, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Sub Categorias"
        unique_together = ('categoria', 'description')

class Unico(models.Model):
    nombre = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk
        super().save(*args, **kwargs)

    @classmethod
    def truncate(cls):
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE "{0}" CASCADE'.format(cls.meta.db_table)) 

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver(post_save, sender=Categoria)
def categoria_saved(sender, **kwargs):
    print ("Categoria Guardada")

@receiver(post_delete, sender=Categoria)
def categoria_deleted(sender, **kwargs):
    print("Categoria Eliminada")

from django.contrib.auth.models import User

class UserParent(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key = True,
    )
    father_name = models.Charfield(max_length=50)
    mother_name = models.CharField(max_length=50)

class Empleado(models.Model):
    supervisor = models.ForeignKey('self', on_delete=models.CASCADE)

class Employee(models.Model):
    supervisor = models.ForeignKey('app1.Employee', on_delete=models.CASCADE)

class ViewCat(models.Model):
    descripcion = models.Charfield(max_length=100)

    class Meta:
        managed = False
        db_table = "categoria_view"

class NombreColumna(models.Model):
    a = models.CharField(max_length = 10, db_column='columna1')
    columna2 = models.CharField(max_length=40)

    def __str__(self):
        return self.a

    class Meta:
        db_table = 'ORM Django'