from django.db import models
from django.db.models import QuerySet

from main.constants import ORDER_STATUS_ACTIVE, ORDER_STATUS_FILLED


class OrderManager(models.Manager):

    def active(self) -> QuerySet:
        return super().get_queryset().filter(status=ORDER_STATUS_ACTIVE)

    def proto(self, proto: 'Proto') -> QuerySet:
        return self.active().filter(asset__proto=proto)


class ProtoManager(models.Manager):

    def active(self) -> QuerySet:
        return super().get_queryset().filter(assets__orders__status=ORDER_STATUS_ACTIVE)
