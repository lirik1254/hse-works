import json

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile
from codeforces.service import get_user_dict
from custom_auth.tasks import redis_client


class UserProfileSerializer(serializers.ModelSerializer):
    codeforces_rating = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'bio', 'university_group', 'codeforces_handle', 'codeforces_rating']

    def get_codeforces_rating(self, obj):
        if obj.codeforces_handle:
            codeforces_data = json.loads(redis_client.get(obj.codeforces_handle))
            if 'rating' in codeforces_data:
                return codeforces_data['rating']
            else:
                return 'Не в рейтинге'
        return None


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(source='userprofile', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'profile']
