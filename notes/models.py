from django.db import models
from app.settings import AUTH_USER_MODEL


class Note(models.Model):
    """
    Modelo de nota.
    """
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=False,
                             null=False)
    description = models.TextField(
        max_length=255, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
        ordering = ['-modified']

    def __str__(self):
        return self.title
