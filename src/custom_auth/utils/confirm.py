from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect, HttpResponse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from token import decode_token
from django.contrib.auth.models import User
from user_profiles.models import UserProfile


def generate_confirmation_link(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    return f"http://127.0.0.1:8000/api/confirm-email/{uid}/{token}/"
