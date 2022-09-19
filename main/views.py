from django.shortcuts import HttpResponseRedirect
from .models import Links, Statistic
from rest_framework import viewsets, status
from django.db.models import F
from rest_framework.response import Response
from .serializers import ShortenedLinkSerializer
from django.conf import settings


def redirect(request, shortened_link_id):
    shortened_link = settings.HOST_URL + shortened_link_id
    link_querset = Links.objects.get(shortened_link=shortened_link)
    original_link = link_querset.original_link

    # Counting the number of visits to a given shortened link
    Statistic.objects.filter(shortened_link_stat=link_querset).update(numbers_of_visits_shortened_link=
                                                                      F('numbers_of_visits_shortened_link') + 1)
    return HttpResponseRedirect(redirect_to=original_link)


class LinkShortener(viewsets.ViewSet):
    """
    "Endpoint": "api/shortener-link"
    "ReturnedForm": {"original_link": str,"shortened_link": str}

    POST: Return JSON with 'original link' and created 'shortened link' if 'original link' was shortened before, return
    already existing shortened link

    :return 200: return already existed shortened url
    :return 201: create new shortened url
    :return 400: serializer error

    """

    serializer_class = ShortenedLinkSerializer

    def create(self, request):

        if Links.objects.filter(original_link=request.data['original_link']).exists():
            serializer_link = ShortenedLinkSerializer(Links.objects.get(original_link=request.data['original_link']))

            return Response(serializer_link.data, status=status.HTTP_200_OK)

        # If IP or User Agent for some reason cannot be downloaded,
        # it gives base values so as not to obstruct the script operation
        ip = request.META.get('REMOTE_ADDR') or '0.0.0.0.0'

        user_agent = request.META.get('HTTP_USER_AGENT') or 'none'

        serializer_link = ShortenedLinkSerializer(data=request.data,
                                                  context={'ip': ip,
                                                           'user_agent': user_agent})

        if not serializer_link.is_valid():
            return Response(serializer_link.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer_link.save()
        return Response(serializer_link.data, status=status.HTTP_201_CREATED)
