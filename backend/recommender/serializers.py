from .models import TalentProfile, CustomeUser, Job, Skill
from rest_framework import serializers 
from django.contrib.auth.hashers import make_password
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job 
        fields = '__all__'
class TalentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TalentProfile
        fields = '__all__'
class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomeUser
        fields = '__all__'
    def validate_password(self, value: str) -> str:
        return make_password(value)