from django.db import models
from ckeditor.fields import RichTextField
from crum import get_current_user
from django.db import models
from django.contrib.auth.models import User
from django.forms import model_to_dict
from solo.models import SingletonModel

# class Base(models.Model):
#     usuario_grabacion = models.ForeignKey(User, on_delete=models.PROTECT, related_name='usuario_grabacion_%(class)s',
#                                           blank=True, null=True)
#     fecha_grabacion = models.DateTimeField(auto_now_add=True)
#     usuario_modificacion = models.ForeignKey(User, related_name='usuario_modificacion_%(class)s',
#                                              on_delete=models.PROTECT, blank=True, null=True)
#     fecha_modificacion = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         abstract = True
#
#     def save(self, *args, **kwargs):
#         #user = get_current_user()
#         user = getattr(self, 'usuario_grabacion', None) or getattr(self, 'usuario_modificacion', None) or getattr(self,'user',None)
#         if user and not user.pk:
#             user = None
#         if not self.pk:
#             self.usuario_grabacion = user
#         self.usuario_modificacion = user
#         super().save(*args, **kwargs)
#
#     def save(self, usuario_actual=None, *args, **kwargs):
#         if usuario_actual and not usuario_actual.pk:
#             usuario_actual = None
#         if not self.pk:
#             self.usuario_grabacion = usuario_actual
#         self.usuario_modificacion = usuario_actual
#         super().save(*args, **kwargs)
#
#     def to_json(self):
#         return model_to_dict(self)

class Base(models.Model):
    usuario_grabacion = models.ForeignKey(User, on_delete=models.PROTECT, related_name='usuario_grabacion_%(class)s',
                                          blank=True, null=True)
    fecha_grabacion = models.DateTimeField(auto_now_add=True)
    usuario_modificacion = models.ForeignKey(User, related_name='usuario_modificacion_%(class)s',
                                             on_delete=models.PROTECT, blank=True, null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.usuario_grabacion = user
        self.usuario_modificacion = user
        super().save(*args, **kwargs)

    def to_json(self):
        return model_to_dict(self)
