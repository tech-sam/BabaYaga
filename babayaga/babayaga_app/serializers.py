from rest_framework import serializers
from babayaga_app.models import DatabseServerProps


class DbPropsSerialzer(serializers.ModelSerializer):
    class Meta:
        model = DatabseServerProps
        fields = '__all__'