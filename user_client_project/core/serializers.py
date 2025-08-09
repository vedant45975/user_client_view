from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Client, Project

class UserShallowSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='username')

    class Meta:
        model = User
        fields = ['id', 'name']

class ProjectSerializer(serializers.ModelSerializer):
    client = serializers.CharField(source='client.client_name', read_only=True)
    users = UserShallowSerializer(many=True, read_only=True)
    created_by = UserShallowSerializer(read_only=True)
    
    assigned_users = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'client', 'users', 'assigned_users', 'created_at', 'created_by']
        read_only_fields = ['id', 'client', 'users', 'created_at', 'created_by']

    def create(self, validated_data):
        assigned_users_data = validated_data.pop('assigned_users', [])
        project = Project.objects.create(**validated_data)
        project.users.set(assigned_users_data)
        return project
    
    def update(self, instance, validated_data):
        assigned_users_data = validated_data.pop('assigned_users', None)
        if assigned_users_data is not None:
            instance.users.set(assigned_users_data)
        
        return super().update(instance, validated_data)


class ProjectNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'project_name']

class ClientSerializer(serializers.ModelSerializer):
    projects = ProjectNestedSerializer(many=True, read_only=True)
    created_by = UserShallowSerializer(read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'created_by', 'updated_at', 'projects']
        read_only_fields = ['id', 'created_at', 'created_by', 'updated_at', 'projects']