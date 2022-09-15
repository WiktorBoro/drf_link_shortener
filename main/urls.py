from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register('shortener-link', views.LinkShortener, basename='Create Shortener Link')


urlpatterns = [
    path('', include(router.urls)),
    path('<shortened_link>', views.redirect, name='Redirecting the shortened link to the original')
]
