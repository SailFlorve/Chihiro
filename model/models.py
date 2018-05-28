from django.db import models


#存放爬虫爬下来的数据


class SourceData(models.Model):
    title = models.CharField(max_length=20)


