# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class MyUser(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='ID')
    username = models.CharField(max_length=255)

    @classmethod
    def get_sharding_model(cls, _id=None):
        piece = _id % 2 + 1

        class Meta:
            db_table = 'user_%s' % piece

        attrs = {
            '__module__': cls.__module__,
            'Meta': Meta,
        }

        Model = type(str('User%s' % piece), (cls, ), attrs)
        return Model

    @classmethod
    def sharding_get(cls, _id=None, **kwargs):
        assert _id, '_id is required!'
        Model = cls.get_sharding_model(_id=_id)
        return Model.objects.get(id=_id, **kwargs)

    class Meta:
        abstract = True


# class User1(MyUser):
    # class Meta:
        # db_table = 'user_1'


# class User2(MyUser):
    # class Meta:
        # db_table = 'user_2'
