from django.db import models
from string import ascii_uppercase, ascii_lowercase, digits
from random import choice
from constance import config
from django.conf import settings


class UsersInfo(models.Model):
    user_agent = models.CharField(max_length=250)
    ip = models.GenericIPAddressField()

    objects = models.Manager()

    def __str__(self):
        return self.ip


class Links(models.Model):
    user_info = models.ForeignKey(UsersInfo, on_delete=models.PROTECT)
    original_link = models.URLField(null=True, max_length=255)
    shortened_link = models.URLField(null=True, max_length=100)

    objects = models.Manager()

    def generate_short_link(self):
        size = config.LENGTH
        chars = str()

        if config.LOWERCASE:
            chars += ascii_lowercase
        if config.DIGITS:
            chars += digits
        if config.UPPERCASE:
            chars += ascii_uppercase

        while True:
            url = ''.join(choice(chars) for _ in range(size))
            if not Links.objects.filter(shortened_link=url).exists():
                break

        return settings.HOST_URL + url

    def save(self, *args, **kwargs):
        if not self.shortened_link:
            self.shortened_link = self.generate_short_link()

        super().save(*args, **kwargs)

        Statistic.objects.create(shortened_link_stat=Links.objects.get(shortened_link=self.shortened_link)).save()

    def __str__(self):
        return self.original_link


class Statistic(models.Model):
    shortened_link_stat = models.ForeignKey(Links, on_delete=models.CASCADE)
    numbers_of_visits_shortened_link = models.SmallIntegerField(default=0)

    objects = models.Manager()

    def __str__(self):
        return self.shortened_link_stat.shortened_link
