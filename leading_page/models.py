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

    def save(self):
        self.description = self.description.upper()
        super(Categoria, self).save()

    class Meta:
        verbose_name_plural = "Sub Categorias"
        unique_together = ('categoria', 'description')
