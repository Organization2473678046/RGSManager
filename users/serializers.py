# -*- coding: utf-8 -*-
from rest_framework import serializers
from models import User


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'isadmin', 'reallyname', 'date_joined']
        extra_kwargs = {'password': {"write_only": True},
                        'reallyname': {"required": True},
                        "date_joined": {"format": '%Y-%m-%d %H:%M:%S'}
                        }

    def create(self, validated_data):
        user = super(UserListSerializer, self).create(validated_data)
        if user.isadmin is True:
            user.set_password("root12345")
        else:
            user.set_password("12345")
        user.save()
        return user


    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "isadmin", "reallyname"]
