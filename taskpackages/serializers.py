# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import serializers
from models import TaskPackage, TaskPackageVersion


class MapListViewSerializer(serializers.ModelSerializer):
    worker = serializers.ReadOnlyField()

    class Meta:
        model = TaskPackage
        fields = ['id', 'name', 'mapnums', 'file', 'status', 'create_time', 'worker']


class CreateMapMessageViewSerializer(serializers.ModelSerializer):
    worker = serializers.IntegerField(max_value=16, write_only=True)

    class Meta:
        model = TaskPackage
        fields = ['name', 'mapnums', 'file', 'describe', 'user_id', 'worker']

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        validated_data['user_id'] = validated_data['worker']
        taskname = validated_data.get('name')
        validated_data['name'] = taskname
        del validated_data['worker']
        taskpackage = super(CreateMapMessageViewSerializer, self).create(validated_data)
        taskpackage.save()

        return taskpackage


class CreateTaskpackageVersionSerializer(serializers.ModelSerializer):
    taskpackage_file_id = serializers.IntegerField(max_value=16, write_only=True)
    worker = serializers.IntegerField(max_value=16, write_only=True)

    class Meta:
        model = TaskPackageVersion
        fields = ['version_name', 'describe', 'file', 'taskpackage_id', 'user_id', 'taskpackage_file_id', 'worker']

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        validated_data['user_id'] = validated_data['worker']
        validated_data['taskpackage_id'] = validated_data['taskpackage_file_id']
        versionnum = TaskPackageVersion.objects.filter(taskpackage_id=validated_data['taskpackage_file_id']).count()
        if versionnum == 0:
            validated_data['version_name'] = validated_data['version_name'] + '_v1.0'
        else:
            validated_data['version_name'] = validated_data['version_name'] + '_v' + str(versionnum + 1) + '.0'
        del validated_data['taskpackage_file_id']
        del validated_data['worker']
        taskpackageversion = super(CreateTaskpackageVersionSerializer, self).create(validated_data)
        taskpackageversion.save()
        return taskpackageversion


class MapVersionListViewSerializer(serializers.ModelSerializer):
    taskpackage_name = serializers.ReadOnlyField()

    class Meta:
        model = TaskPackageVersion
        fields = ['id', 'version_name', 'file', 'status', 'create_time', 'describe', 'taskpackage_name']
