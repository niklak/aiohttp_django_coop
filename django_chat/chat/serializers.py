from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password as vp
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from . import models


class AbsChannelSerializer(serializers.ModelSerializer):
    starter = serializers.SerializerMethodField(read_only=True)

    def get_starter(self, obj):
        return obj.started_by.username


class ChannelSerializer(AbsChannelSerializer):

    class Meta:
        model = models.Channel


class BriefChannelSerializer(AbsChannelSerializer):

    class Meta:
        model = models.Channel
        fields = ('id', 'title', 'started_by')


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField(read_only=True)

    def get_sender(self, obj):
        return obj.sender.username

    class Meta:
        model = models.Message
        fields = ('text', 'create_date', 'sender')


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(allow_blank=False, write_only=True)

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('confirm_password'):
            raise serializers.ValidationError({'confirm_password':
                                                   _('Passwords do not match')})
        return attrs

    def validate_password(self, value):
        vp(value)
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ('password', 'confirm_password',
                  'username')
        write_only_fields = ('password',)