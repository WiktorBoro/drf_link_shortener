from django.shortcuts import HttpResponseRedirect
from .models import Links, Statistic
from rest_framework import viewsets, status
from django.db.models import F
from rest_framework.response import Response
from .serializers import LinkInputSerializer,  ShortenedLinkSerializer
from django.conf import settings


def redirect(request, shortened_link_id):
    shortened_link = settings.HOST_URL + settings.SHORTENED_LINK_ALIAS + shortened_link_id
    link_querset = Links.objects.get(shortened_link=shortened_link)
    original_link = link_querset.original_link

    Statistic.objects.filter(shortened_link_stat=link_querset).update(numbers_of_visits_shortened_link=
                                                                      F('numbers_of_visits_shortened_link') + 1)
    return HttpResponseRedirect(redirect_to=original_link)


class LinkShortener(viewsets.ViewSet):
    serializer_class = LinkInputSerializer

    def create(self, request, *args, **kwargs):

        if Links.objects.filter(original_link=request.data['original_link']).exists():
            serializer = ShortenedLinkSerializer(Links.objects.get(original_link=request.data['original_link']))

            return Response(serializer.data, status=status.HTTP_200_OK)
        ip = request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT')
        serializer = ShortenedLinkSerializer(data=request.data, context={'ip': ip,
                                                                         'user_agent': user_agent})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # if link := Links.objects.get(original_link=serializer.data['original_link']):
        #     print('xxx', serializer.validated_data)
        #     return Response(serializer.data+{'link': link.shortened_link}, status=status.HTTP_200_OK)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
