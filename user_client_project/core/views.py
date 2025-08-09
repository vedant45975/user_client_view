from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer, UserShallowSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set the `created_by` field to the current user
        serializer.save(created_by=self.request.user)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retrieve only the projects assigned to the logged-in user
        return Project.objects.filter(users=self.request.user)

class ProjectCreateForClientView(generics.CreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        client_id = self.kwargs.get('client_id')
        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            return Response({'error': 'Client not found.'}, status=status.HTTP_404_NOT_FOUND)

        assigned_users_data = request.data.pop('users', [])
        user_ids = [user['id'] for user in assigned_users_data]

        serializer = self.get_serializer(data={
            'project_name': request.data.get('project_name'),
            'assigned_users': user_ids
        })
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer, client=client)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer, client):
        serializer.save(client=client, created_by=self.request.user)