# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class MyUser(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name='ID')
    username = models.CharField(max_length=255)

    @classmethod
    def get_sharding_table(cls, id=None):
        piece = id % 2 + 1
        return cls._meta.db_table + str(piece)

    @classmethod
    def sharding_get(cls, id=None, **kwargs):
        assert isinstance(id, int), 'id must be integer!'
        table = cls.get_sharding_table(id)
        sql = "SELECT * FROM %s" % table
        kwargs['id'] = id
        condition = ' AND '.join([k + '=%s' for k in kwargs])
        params = [str(v) for v in kwargs.values()]
        where = " WHERE " + condition
        try:
            return cls.objects.raw(sql + where, params=params)[0]  # 这里应该模仿Queryset中get的处理方式
        except IndexError:
            # 其实应该抛Django的那个DoesNotExist异常
            return None

    class Meta:
        db_table = 'user_'


# class User1(MyUser):
    # class Meta:
        # db_table = 'user_1'


# class User2(MyUser):
    # class Meta:
        # db_table = 'user_2'
