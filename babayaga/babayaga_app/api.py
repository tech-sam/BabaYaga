from babayaga_app.models import DatabseServerProps
from rest_framework import viewsets, permissions
from .serializers import DbPropsSerialzer


class DbPropsViewSet(viewsets.ModelViewSet):
    queryset = DatabseServerProps.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = DbPropsSerialzer
