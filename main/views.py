from django.shortcuts import HttpResponseRedirect
from .models import Statistic, Links, Statistic
from rest_framework import viewsets, status
from django.db.models import F
from rest_framework.response import Response
from .serializers import LinkShortenerSerializer
from django.shortcuts import get_object_or_404


def redirect(request, shortened_link):
    original_link = Links.objects.get(shortened_link=shortened_link).original_link
    Statistic.objects.get(shortened_link=shortened_link).update(numbers_of_visits_shortened_link=
                                                                F('numbers_of_visits_shortened_link')+1)
    return HttpResponseRedirect(redirect_to=original_link)


class LinkShortener(viewsets.ModelViewSet):
    queryset = Links.objects.all()
    serializer_class = LinkShortenerSerializer
    http_method_names = ['post']


# class LinkShortener(viewsets.ViewSet):
#     lookup_field = 'original_link'
#     serializer_class = LinkShortenerSerializer
#
#     def list(self, request):
#         queryset = Links.objects.all()
#         serializer_user = LinkShortenerSerializer(queryset, many=True)
#         return Response(serializer_user.data, status=status.HTTP_200_OK)
#
#     def create(self, request):
#         serializer_link = LinkShortenerSerializer(data=request.data)
#
#         if not serializer_link.is_valid():
#             return Response(serializer_link.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         queryset = Links.objects.filter(original_link=serializer_link.original_link)
#         if queryset:
#             return Response(serializer_user.data, status=status.HTTP_201_CREATED)
#
#         serializer_user.save()
#         return Response(serializer_user.data, status=status.HTTP_201_CREATED)