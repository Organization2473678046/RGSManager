# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import serializers
from models import Users


class CreateUserSerizlizer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'password', 'is_admin']

    def create(self, validated_data):
        user = super(CreateUserSerizlizer, self).create(validated_data=validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user


class UserMessageList(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'is_admin']


class WorkerListSerialziers(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username']
