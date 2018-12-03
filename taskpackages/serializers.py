# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import serializers
from models import Files



class MapListViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = ['id', 'filename', 'mapnum', 'filepath', 'status', 'create_time']



class CreateMapMessageViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = ['filename', 'mapnum', 'filepath', 'status', 'work_user']

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        """
        from django.utils import timezone
        filename = validated_data['work_user'] + validated_data.get("filename") + timezone.now().strftime('%Y%m%d%H%M%S%f')
        """
        filename = validated_data.get("filename")
        validated_data['filename'] = filename
        mapfile = super(CreateMapMessageViewSerializer, self).create(validated_data)
        mapfile.save()

        return mapfile

