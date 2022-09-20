from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status
from django.conf import settings


# class TestSetUp(APITestCase):
class TestShortenerLinkApi(APITestCase):

    def test_should_return_correct_response(self):

        url = 'https://www.django-rest-framework.org/api-guide/testing/'

        response = self.client.post('/api/shortener-link',
                                    data={'original_link': url},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['original_link'], url)
        self.assertIn(settings.HOST_URL, response.data['shortened_link'])
        self.assertRegex(response.data['shortened_link'], f'{settings.HOST_URL}[^\/\!\?\=\+\-]+')

    def test_should_return_already_exist_link(self):

        url = 'https://www.django-rest-framework.org/api-guide/testing/'

        response_1 = self.client.post('/api/shortener-link',
                                      data={'original_link': url},
                                      format='json')

        response_2 = self.client.post('/api/shortener-link',
                                      data={'original_link': url},
                                      format='json')
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        self.assertIn(settings.HOST_URL, response_2.data['shortened_link'])
        self.assertEqual(response_2.data['shortened_link'], response_2.data['shortened_link'])

    def test_should_return_empty_error(self):

        response = self.client.post('/api/shortener-link',
                                    data={'original_link': ''},
                                    format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['original_link'][0], 'This field may not be blank.')

    def test_should_return_incorrect_url_error(self):

        url = 'test'

        response = self.client.post('/api/shortener-link',
                                    data={'original_link': url},
                                    format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['original_link'][0], 'Enter a valid URL.')
