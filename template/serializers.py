# 두 번째 개발 : 객체를 일련의 데이터로 변환
from rest_framework import serializers
from .models import Template

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Template
        fields = '__all__'