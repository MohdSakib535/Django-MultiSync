from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Record, SyncStatus
from .serializers import RecordSerializer, SyncStatusSerializer
from .tasks import sync_to_read_database

class RecordCreateView(APIView):
    """
    POST endpoint to create a new record.
    The record is saved in MySQL (default) and a Celery task is triggered
    to sync it to PostgreSQL.
    """
    def post(self, request, format=None):
        serializer = RecordSerializer(data=request.data)
        if serializer.is_valid():
            record = serializer.save()  # saved in default DB (MySQL)
            # Trigger Celery task to sync to read_db (Postgres)
            sync_to_read_database.delay(record.id)  # Trigger Celery Task
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecordListView(APIView):
    """
    GET endpoint to list all records from the read database (PostgreSQL).
    """
    def get(self, request, format=None):
        # Fetch records from PostgreSQL using the 'read_db' alias
        records = Record.objects.using('read_db').all()
        serializer = RecordSerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SyncStatusListView(APIView):
    """
    GET endpoint to list all sync status entries.
    """
    def get(self, request, format=None):
        statuses = SyncStatus.objects.all()
        serializer = SyncStatusSerializer(statuses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
