from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile
from codeforces.service import get_user_dict


class UserProfileSerializer(serializers.ModelSerializer):
    codeforces_rating = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'bio', 'university_group', 'codeforces_handle', 'codeforces_rating']

    def get_codeforces_rating(self, obj):
        if obj.codeforces_handle:
            codeforces_data = get_user_dict(obj.codeforces_handle)
            return codeforces_data['rating']
        return None


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(source='userprofile', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'profile']
