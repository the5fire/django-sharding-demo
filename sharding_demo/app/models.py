# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class MyUser(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='ID')
    username = models.CharField(max_length=255)

    class Meta:
        abstract = True


class User01(MyUser):
    class Meta:
        db_table = 'user_01'


class User02(MyUser):
    class Meta:
        db_table = 'user_02'
