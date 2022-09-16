from rest_framework import serializers
from .models import Links, UsersInfo


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersInfo
        fields = ('user_agent', 'ip')

    def create(self, data):
        users_info = UsersInfo.objects.get_or_create(ip=self.context.get('ip'),
                                                     user_agent=self.context.get('user_agent'))

        return users_info


class ShortenedLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Links
        fields = ['original_link', 'shortened_link']

    def create(self, data):
        user_info, user_exist = UsersInfo.objects.get_or_create(user_agent=self.context.get('user_agent'),
                                                                ip=self.context.get('ip'))
        shortened_link, link_exist = Links.objects.get_or_create(original_link=data['original_link'],
                                                                 user_info=user_info)
        # if link_exist:
        #     return shortened_link, link_exist

        return shortened_link


class LinkInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Links
        fields = ['original_link']
