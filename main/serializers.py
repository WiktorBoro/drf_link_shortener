from rest_framework import serializers
from .models import Links, UsersInfo


class ShortenedLinkSerializer(serializers.ModelSerializer):
    shortened_link = serializers.URLField(read_only=True)

    class Meta:
        model = Links
        fields = ['original_link', 'shortened_link']
        extra_kwargs = {'original_link': {'required': True,
                                          'allow_null': False}}

    def create(self, data):
        user_info, user_exist = UsersInfo.objects.get_or_create(user_agent=self.context.get('user_agent'),
                                                                ip=self.context.get('ip'))

        shortened_link = Links.objects.create(original_link=data['original_link'],
                                              user_info=user_info)

        return shortened_link
