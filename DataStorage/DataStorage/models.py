from django.db import models
import json

# Create your models here.


class Data(models.Model):
    key = models.CharField(max_length=100, verbose_name="键")
    value = models.TextField(verbose_name="值", blank=True)
    createtime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updatetime = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        verbose_name_plural = '数据'
        ordering = ['-updatetime']

    def __str__(self):
        return '%s' % self.key

    def to_dict(self):
        try:
            _value = json.loads(self.value)
        except:
            _value = self.value
        return {
            self.key: _value,
            "createtime": self.createtime,
            "updatetime": self.updatetime
        }

    def format_value(self):
        if len(self.value) < 50:
            return self.value
        return f'{self.value[:25]}...{self.value[-25:]}'

    format_value.short_description = "值"
    format_value.allow_tags = True
