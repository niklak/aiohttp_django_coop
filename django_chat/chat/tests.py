from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from rest_framework.authtoken.models import Token
from .models import Channel, Message

METHODS = ['head', 'get', 'post', 'put', 'patch', 'trace', 'delete']


# Create your tests here.
class ChatTests(APITestCase):

    allowed = ['get', 'head']

    def setUp(self):
        self.user_list = [{'username': 'rick', 'password': 'wubba-lubba'},
                          {'username': 'morty', 'password': 'jessica'},
                          {'username': 'jerry', 'password': 'jerry'}]

        User = get_user_model()
        for user in self.user_list:
            row = User(username=user['username'])
            row.set_password(user['password'])
            row.save()
        self.users = User.objects.all().order_by('id')

        starter = self.users.first()
        self.channel_list = [
            {'title': 'Morty`s room', 'started_by': starter},
            {'title': 'Ricks`s garage', 'started_by': starter,
             'topic': 'Denied for Jerry'},
            {'title': 'Jerry`s own', 'started_by': starter,
             'is_closed': True},
        ]
        for d in self.channel_list:
            Channel(**d).save()
        self.channels = Channel.opened.all()

        base_message = 'Hello from {}!'
        channel = self.channels.first()

        bulk = (Message(text=base_message.format(user.username),
                        sender=user, channel=channel) for user in self.users)

        Message.objects.bulk_create(bulk)

        self.token = Token.objects.get(user__username=
                                       self.user_list[0]['username'])
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_db_table_message_row_count(self):
        channel = Channel.opened.first()
        message_count = Message.objects.filter(channel=channel).count()
        user_count = len(self.users)
        self.assertEqual(message_count, user_count, 'Wrong message count')

    def test_obtain_token(self):
        user = self.user_list[0]
        url = reverse('api-token-auth')
        client = APIClient()
        response = client.post(url, data=user)
        self.assertEqual(response.data['token'], self.token.key)

    def test_login(self):
        user_c = self.user_list[0]
        user = self.users.first()
        data_compare = {'username': user.username, 'token': self.token.key, 'id': user.id}
        url = reverse('chat:login')
        client = APIClient()
        response = client.post(url, data=user_c)
        self.assertEqual(response.data, data_compare)

    def test_users(self):
        for n, user in enumerate(self.users):
            self.assertTrue(user.check_password(self.user_list[n]['password']),
                            'Passwords do not match')

    def test_channel_list_statuses(self):

        url = reverse('chat:channel-list')

        for method in METHODS:
            self.method_access(method, url)

    def test_channel_detail_statuses(self):
        for channel in self.channels:
            allowed = ['get', 'post', 'head']
            url = reverse('chat:channel-detail', kwargs={'pk': channel.id})
            for method in METHODS:
                self.method_access(method, url, allowed=allowed)

    def test_message_list_statuses(self):
        for channel in self.channels:
            url = reverse('chat:message-list', kwargs={'pk': channel.id})
            for method in METHODS:
                self.method_access(method, url)

    def test_closed_channels(self):
        closed = Channel.objects.filter(is_closed=True).first()
        url = reverse('chat:channel-detail', kwargs={'pk': closed.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_create_channel(self):
        url = reverse('chat:channel-list')
        data = {'started_by': self.users.first().id,
                'title': 'test', 'topic': 'first'}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def method_access(self, method, url, allowed=None):
        allowed = self.allowed if allowed is None else allowed
        if method in allowed:
            s = status.HTTP_200_OK
        else:
            s = status.HTTP_405_METHOD_NOT_ALLOWED

        req = getattr(self.client, method)
        response = req(url)
        self.assertEqual(response.status_code, s, 'Method %s, %s' % (method, response.data))