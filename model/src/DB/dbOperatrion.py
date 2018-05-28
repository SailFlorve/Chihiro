# -*- coding: utf-8 -*-

from django.http import HttpResponse

from model.models import SourceData


# 数据库操作示例


def add_data(request):
    test1 = SourceData(name='runoob')
    test1.save()


def update_data(request):
    # 修改其中一个id=1的name字段，再save，相当于SQL中的UPDATE
    test1 = SourceData.objects.get(id=1)
    test1.name = 'Google'
    test1.save()

    # 另外一种方式
    # SourceData.objects.filter(id=1).update(name='Google')

    # 修改所有的列
    # SourceData.objects.all().update(name='Google')


def delete_data(request):
    # 删除id=1的数据
    test1 = SourceData.objects.get(id=1)
    test1.delete()

    # 另外一种方式
    # SourceData.objects.filter(id=1).delete()

    # 删除所有数据
    # SourceData.objects.all().delete()







def get_data(request):
    # 初始化
    response = ""
    response1 = ""

    # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM
    list = SourceData.objects.all()

    # filter相当于SQL中的WHERE，可设置条件过滤结果
    response2 = SourceData.objects.filter(id=1)

    # 获取单个对象
    response3 = SourceData.objects.get(id=1)

    # 限制返回的数据 相当于 SQL 中的 OFFSET 0 LIMIT 2;
    SourceData.objects.order_by('name')[0:2]

    # 数据排序
    SourceData.objects.order_by("id")

    # 上面的方法可以连锁使用
    SourceData.objects.filter(name="runoob").order_by("id")





