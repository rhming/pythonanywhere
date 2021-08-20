from django.db import models

# Create your models here.


class Data(models.Model):

    key = models.CharField(max_length=100, unique=True, verbose_name="键")
    value = models.TextField(verbose_name="值")
    createtime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    class Meta:
        verbose_name_plural = '数据'

    def __str__(self):
        return '%s' % self.key

    def format_value(self):
        if len(self.value) < 50:
            return self.value
        else:
            return f'{self.value[:25]}...{self.value[-25:]}'

    format_value.allow_tags = True

