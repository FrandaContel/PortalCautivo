from django.db import models
from django.utils.timezone import now
# Create your models here.

class mac_users(models.Model):
    macaddrs = models.CharField(max_length=20)
    hora = models.DateTimeField(default=now)

    def __str__(self) -> str:
        return super().__str__(self.macaddrs + ' ' + self.hora)