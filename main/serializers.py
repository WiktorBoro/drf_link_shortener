from rest_framework import serializers
from .models import Links


class LinkShortenerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Links
        fields = '__all__'

    def create(self, data):
        print("serializacja danych", data)
        shortened_link = Links.objects.get_or_create(**data)

        return shortened_link
