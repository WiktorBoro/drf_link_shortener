from django.db import models
from .valid_models import validate_links_scope, validate_links_length
from .short_link_generator import short_link_generator
from django.core.validators import MaxValueValidator, MinValueValidator


class UsersInfo(models.Model):
    user_agent = models.CharField(max_length=250)
    ip = models.GenericIPAddressField()

    objects = models.Manager()

    def __str__(self):
        return self.ip


class Links(models.Model):
    user_info = models.ForeignKey(UsersInfo, on_delete=models.CASCADE)
    original_link = models.CharField(max_length=255, unique=True)
    shortened_link = models.CharField(default=short_link_generator(), max_length=100)

    objects = models.Manager()

    def __str__(self):
        return self.original_link


class Statistic(models.Model):
    shortened_link = models.ForeignKey(Links, on_delete=models.CASCADE)
    numbers_of_visits_shortened_link = models.SmallIntegerField()

    objects = models.Manager()

    def __str__(self):
        return self.shortened_link

# class ShortenedLinkSettings(models.Model):
#     length_of_the_shortened_link = models.SmallIntegerField(default=5,
#                                                             validators=[
#                                                                         MaxValueValidator(100),
#                                                                         MinValueValidator(5)
#                                                                         ])
#     digits = models.BooleanField(default=True)
#     uppercase = models.BooleanField(default=True)
#     lowercase = models.BooleanField(default=True)
#
#     objects = models.Manager()



