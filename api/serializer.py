from api.models import * 
from rest_framework import serializers

class addPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = "__all__"

class readPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = People
        fields = ['id', 'parent', 'name', 'role', 'is_parent']  # Specify only the needed fields