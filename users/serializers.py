# -*- coding: utf-8 -*-
from rest_framework import serializers
from models import User


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'isadmin', 'reallyname']
        extra_kwargs = {'password': {"write_only": True},'isadmin': {"write_only": True},'reallyname':{"required":True}}


    def create(self, validated_data):
        user = super(UserListSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()

        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username","isadmin","reallyname"]
