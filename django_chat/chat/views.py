from django.contrib.auth import logout, login
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import generics, mixins
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token

from social.apps.django_app.utils import load_backend, load_strategy
from social.backends.oauth import BaseOAuth1, BaseOAuth2
from social.exceptions import AuthAlreadyAssociated

from . import models, serializers
# Create your views here.


class ChannelView(mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                  generics.GenericAPIView):

    queryset = models.Channel.opened.select_related('started_by')
    pagination_class = None
    serializer_class = serializers.ChannelSerializer

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk'):
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer_class = serializers.BriefChannelSerializer
        serializer = serializer_class(queryset, many=True,
                                      context={'request': request})
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if kwargs.get('pk'):
            return self.retrieve(request, *args, **kwargs)
        return self.create(request, *args, **kwargs)


@api_view(['GET', 'HEAD'])
def message_list(request, pk):
    """
    You should implement a pagination for your own purpose.
    Currently, there is no pagination at all.
    """
    messages = models.Message.objects.\
        select_related('sender').filter(channel_id=pk)
    serializer = serializers.MessageSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes(())
def login_view(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    token = Token.objects.get(user=user)
    login(request, user)
    return Response({'token': token.key,
                     'username': user.username, 'id': user.id})


@api_view(['GET'])
def logout_view(request):
    logout(request)
    return Response(status=200)


@api_view(['POST'])
@permission_classes(())
def register_view(request):
    serializer = serializers.UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response(status=201)


@api_view(['GET', 'POST'])
@permission_classes(())
def logged_view(request):
    user = request.user
    if user.is_authenticated():
        token = Token.objects.get(user=user)
        # SET COOKIE HERE!!!
        response = HttpResponseRedirect(reverse('index'))
        response.set_cookie('token', token.key)
        response.set_cookie('l', user.username)
        response.set_cookie('id', user.id)
        return response
    else:
        return Response(status=400)


@api_view(['POST'])
@permission_classes(())
def social_sign_up(request):
    data = {}
    status = 400
    try:
        provider = request.data['provider']
        a_user = request.user if not request.user.is_anonymous() else None
        strategy = load_strategy(request)
        backend = load_backend(strategy=strategy, name=provider,
                               redirect_uri=None)
        if isinstance(backend, BaseOAuth1):
            access_token = {
                'oauth_token': request.data['access_token'],
                'oauth_token_secret': request.data['access_token_secret'],
            }
        else:
            # We assume that if our backend is not instance of BaseOAuth1,
            # it is instance of BaseOAuth2
            access_token = request.data['access_token']

        user = backend.do_auth(access_token, user=a_user)

        if user and user.is_active:
            social = user.social_auth.get(provider=provider)
            if social.extra_data['access_token']:
                social.extra_data['access_token'] = access_token
                social.save()

        login(request, user)
        token = Token.objects.get(user=user)
        data = {'username': user.username, 'id': user.id, 'token': token.key}
        status = 200

    except KeyError as k:
        data['detail'] = ['{} parameter is missed'.format(k)]

    except Exception as exc:
        data['detail'] = [str(exc)]
    finally:
        return Response(data, status=status)
